import os
import requests
import json
from datetime import datetime
import sys
import argparse

# --- Configurações ---

# Configurações do DefectDojo (lidas do ambiente)
DEFECTDOJO_URL = os.environ.get("DEFECTDOJO_URL", "http://localhost:8080")
DEFECTDOJO_TOKEN = os.environ.get("DEFECTDOJO_TOKEN")
PRODUCT_TYPE_NAME = "SAST (Semgrep)"
# O nome do engagement será estático para garantir a deduplicação.
ENGAGEMENT_NAME = "Semgrep Scan (CI)"
# O tipo de scan no DefectDojo deve corresponder ao formato do arquivo.
SCAN_TYPE = "SARIF" 

# --- Fim das Configurações ---

def handle_api_error(e, step):
    """Lida com erros de API de forma padronizada."""
    print(f"[ERRO FATAL] Falha durante a etapa: '{step}'.", file=sys.stderr)
    if hasattr(e, 'response') and e.response is not None:
        print(f"       Status: {e.response.status_code}", file=sys.stderr)
        try:
            print(f"       Mensagem: {e.response.json()}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"       Resposta (não-JSON): {e.response.text}", file=sys.stderr)
    else:
        print(f"       Erro: {e}", file=sys.stderr)
    sys.exit(1)

def get_defectdojo_id_by_name(session, endpoint, name, resource_type):
    """Função genérica para buscar o ID de um recurso do DefectDojo pelo nome."""
    print(f"🔎 Buscando ID para {resource_type} '{name}'...")
    try:
        response = session.get(f"{DEFECTDOJO_URL}/api/v2/{endpoint}/", params={'name': name}, timeout=30)
        response.raise_for_status()
        results = response.json().get('results', [])
        if not results:
            print(f"  -> {resource_type} '{name}' não encontrado.")
            return None
        resource_id = results[0]['id']
        print(f"  -> {resource_type} encontrado com ID: {resource_id}")
        return resource_id
    except requests.exceptions.RequestException as e:
        handle_api_error(e, f"Busca de ID para {resource_type} '{name}'")

def get_or_create_product(session, name, product_type_id):
    """Busca um produto pelo nome ou o cria se não existir."""
    product_id = get_defectdojo_id_by_name(session, "products", name, "Produto")
    if product_id: return product_id

    print(f"  -> Criando produto '{name}'...")
    payload = {"name": name, "description": "Produto criado automaticamente para importação do Semgrep.", "prod_type": product_type_id}
    try:
        response = session.post(f"{DEFECTDOJO_URL}/api/v2/products/", json=payload, timeout=30)
        response.raise_for_status()
        new_product_id = response.json()['id']
        print(f"  -> Produto criado com sucesso com ID: {new_product_id}")
        return new_product_id
    except requests.exceptions.RequestException as e:
        handle_api_error(e, f"Criação do produto '{name}'")

def get_or_create_engagement(session, product_id, engagement_name):
    """Verifica se um engagement contínuo de CI/CD existe ou o cria, retornando seu ID."""
    print(f"🔎 Verificando/Criando engagement contínuo '{engagement_name}'...")
    try:
        # Busca por um engagement ativo com o nome exato
        response = session.get(f"{DEFECTDOJO_URL}/api/v2/engagements/", params={'name': engagement_name, 'product': product_id}, timeout=30)
        response.raise_for_status()
        results = response.json().get('results', [])
        if results:
            eng_id = results[0]['id']
            print(f"  -> Engagement contínuo encontrado com ID: {eng_id}")
            return eng_id
    except requests.exceptions.RequestException as e:
        handle_api_error(e, f"Busca de engagement para o produto {product_id}")

    print(f"  -> Engagement contínuo não encontrado. Criando...")
    today = datetime.now().strftime("%Y-%m-%d")
    payload = {"name": engagement_name, "product": product_id, "target_start": today, "target_end": today, "engagement_type": "CI/CD", "status": "In Progress"}
    try:
        response = session.post(f"{DEFECTDOJO_URL}/api/v2/engagements/", json=payload, timeout=30)
        response.raise_for_status()
        new_eng_id = response.json()['id']
        print(f"  -> Engagement criado com sucesso com ID: {new_eng_id}")
        return new_eng_id
    except requests.exceptions.RequestException as e:
        handle_api_error(e, f"Criação de engagement para o produto {product_id}")

def import_report_to_dojo(session, engagement_id, report_filename):
    """Faz o upload do arquivo de relatório para o DefectDojo."""
    print(f"🚀 Disparando importação do relatório '{report_filename}' para o engagement ID {engagement_id}...")
    try:
        with open(report_filename, 'rb') as f_upload:
            payload = {"scan_type": SCAN_TYPE, "engagement": str(engagement_id), "close_old_findings": "true"}
            files = {'file': (os.path.basename(report_filename), f_upload, 'application/json')}
            response = session.post(f"{DEFECTDOJO_URL}/api/v2/import-scan/", data=payload, files=files, timeout=120)
            response.raise_for_status()
            data = response.json()
            print(f"✅ [SUCESSO] Pedido de importação concluído. Test ID: {data.get('test')}")
    except requests.exceptions.RequestException as e:
        handle_api_error(e, f"Disparo da importação para o engagement {engagement_id}")

def main():
    """Função principal para orquestrar o processo de importação."""
    parser = argparse.ArgumentParser(description="Importa um relatório de scan (SARIF/JSON) para o DefectDojo.")
    parser.add_argument("--report-file", required=True, help="Caminho para o arquivo de relatório a ser importado.")
    parser.add_argument("--project-name", help="Nome do projeto no DefectDojo. Padrão: nome do repositório no GitHub Actions ou 'default-project'.")
    args = parser.parse_args()
    
    # No GitHub Actions, a variável GITHUB_REPOSITORY é 'owner/repo'. Usamos a parte 'repo'.
    default_project_name = os.environ.get("GITHUB_REPOSITORY", "default-project").split('/')[-1]
    project_name = args.project_name or default_project_name
    report_filename = args.report_file

    print(f"Iniciando importação do relatório '{report_filename}' para o DefectDojo...")
    
    if not os.path.exists(report_filename):
        print(f"[ERRO FATAL] O arquivo de relatório '{report_filename}' não foi encontrado.", file=sys.stderr)
        sys.exit(1)
        
    if not DEFECTDOJO_TOKEN:
        print("[ERRO FATAL] A variável de ambiente DEFECTDOJO_TOKEN deve ser configurada.")
        sys.exit(1)

    defectdojo_session = requests.Session()
    defectdojo_session.headers.update({"Authorization": f"Token {DEFECTDOJO_TOKEN}"})

    try:
        # 1. Obter ID do Tipo de Produto
        product_type_id = get_defectdojo_id_by_name(defectdojo_session, "product_types", PRODUCT_TYPE_NAME, "Tipo de Produto")
        if not product_type_id: sys.exit(1)

        # 2. Criar ou Obter Produto
        product_name_dd = f"{project_name} (Semgrep)"
        print(f"  -> Nome do produto no DefectDojo: '{product_name_dd}'")
        product_id = get_or_create_product(defectdojo_session, product_name_dd, product_type_id)

        # 3. Criar ou Obter Engagement de CI
        engagement_id = get_or_create_engagement(defectdojo_session, product_id, ENGAGEMENT_NAME)

        # 4. Importar Scan
        import_report_to_dojo(defectdojo_session, engagement_id, report_filename)
    
    except Exception as e:
        print(f"[ERRO FATAL] Ocorreu uma exceção não tratada: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n[PROCESSO CONCLUÍDO]")

if __name__ == "__main__":
    main() 