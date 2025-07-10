#!/usr/bin/env python3
"""
Script para gerar relatório HTML a partir dos resultados SARIF do Semgrep
"""
import json
import html
import sys
from datetime import datetime
from pathlib import Path

def generate_html_report(sarif_file_path, output_file_path):
    """
    Gera um relatório HTML a partir de um arquivo SARIF
    
    Args:
        sarif_file_path: Caminho para o arquivo SARIF
        output_file_path: Caminho para o arquivo HTML de saída
    """
    
    # Verificar se o arquivo SARIF existe
    if not Path(sarif_file_path).exists():
        print(f"Erro: Arquivo SARIF não encontrado: {sarif_file_path}")
        sys.exit(1)
    
    try:
        # Ler o arquivo SARIF
        with open(sarif_file_path, 'r', encoding='utf-8') as f:
            sarif_data = json.load(f)
    except Exception as e:
        print(f"Erro ao ler arquivo SARIF: {e}")
        sys.exit(1)
    
    # Criar HTML básico
    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Segurança - Semgrep</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .summary {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            border-left: 4px solid #007bff;
        }}
        .result {{
            border: 1px solid #e9ecef;
            margin: 15px 0;
            padding: 20px;
            border-radius: 8px;
            background-color: #ffffff;
        }}
        .result.error {{
            border-left: 5px solid #dc3545;
            background-color: #fff5f5;
        }}
        .result.warning {{
            border-left: 5px solid #fd7e14;
            background-color: #fffaf0;
        }}
        .result.info {{
            border-left: 5px solid #17a2b8;
            background-color: #f0f8ff;
        }}
        .rule-id {{
            font-weight: 600;
            color: #495057;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .message {{
            margin: 15px 0;
            line-height: 1.6;
            color: #333;
        }}
        .location {{
            font-size: 0.9em;
            color: #6c757d;
            background-color: #f8f9fa;
            padding: 8px 12px;
            border-radius: 4px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
        }}
        .no-issues {{
            text-align: center;
            padding: 60px 20px;
            color: #28a745;
        }}
        .no-issues h2 {{
            font-size: 2em;
            margin-bottom: 20px;
        }}
        .severity-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 10px;
        }}
        .severity-error {{
            background-color: #dc3545;
            color: white;
        }}
        .severity-warning {{
            background-color: #fd7e14;
            color: white;
        }}
        .severity-info {{
            background-color: #17a2b8;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Relatório de Segurança</h1>
            <p>Análise realizada com Semgrep em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
        <div class="content">
'''
    
    # Processar resultados
    total_issues = 0
    issues_by_severity = {'error': 0, 'warning': 0, 'info': 0}
    
    if 'runs' in sarif_data and sarif_data['runs']:
        for run in sarif_data['runs']:
            if 'results' in run and run['results']:
                # Construir um mapa das regras para obter severidades
                rules_map = {}
                if 'tool' in run and 'driver' in run['tool'] and 'rules' in run['tool']['driver']:
                    for rule in run['tool']['driver']['rules']:
                        rule_id = rule.get('id', '')
                        default_level = rule.get('defaultConfiguration', {}).get('level', 'info')
                        rules_map[rule_id] = default_level
                
                # Filtrar resultados válidos (não do próprio arquivo SARIF)
                valid_results = []
                seen_results = set()  # Para deduplicação
                
                for result in run['results']:
                    rule_id = result.get('ruleId', '')
                    
                    # Verificar se tem localizações válidas
                    if 'locations' in result and result['locations']:
                        for location in result['locations']:
                            if 'physicalLocation' in location:
                                artifact_location = location['physicalLocation'].get('artifactLocation', {})
                                uri = artifact_location.get('uri', '')
                                
                                # Filtrar resultados que apontam para arquivos SARIF
                                if not uri.endswith('.sarif'):
                                    region = location['physicalLocation'].get('region', {})
                                    start_line = region.get('startLine', 0)
                                    
                                    # Criar uma chave única para deduplicação
                                    unique_key = f"{rule_id}:{uri}:{start_line}"
                                    
                                    if unique_key not in seen_results:
                                        seen_results.add(unique_key)
                                        valid_results.append(result)
                                        break  # Usar apenas a primeira localização válida
                
                total_issues = len(valid_results)
                
                # Contar issues por severidade usando o mapa de regras
                for result in valid_results:
                    rule_id = result.get('ruleId', '')
                    level = rules_map.get(rule_id, 'info')
                    if level in issues_by_severity:
                        issues_by_severity[level] += 1
                
                # Adicionar resumo
                html_content += f'''
            <div class="summary">
                <h2>📊 Resumo da Análise</h2>
                <p><strong>Total de problemas encontrados:</strong> {total_issues}</p>
                <p>
                    <strong>Críticos:</strong> {issues_by_severity['error']} | 
                    <strong>Avisos:</strong> {issues_by_severity['warning']} | 
                    <strong>Informativos:</strong> {issues_by_severity['info']}
                </p>
            </div>
                '''
                
                if valid_results:
                    html_content += '<h2>🔍 Detalhes dos Problemas</h2>'
                    
                    # Processar cada resultado válido
                    for result in valid_results:
                        rule_id = result.get('ruleId', 'N/A')
                        message = result.get('message', {}).get('text', 'N/A')
                        level = rules_map.get(rule_id, 'info')
                        
                        # Mapear níveis do SARIF para classes CSS
                        css_class = {
                            'error': 'error',
                            'warning': 'warning',
                            'info': 'info',
                            'note': 'info'
                        }.get(level, 'info')
                        
                        # Mapear para badges de severidade
                        severity_badge = f'<span class="severity-badge severity-{css_class}">{level}</span>'
                        
                        html_content += f'''
                <div class="result {css_class}">
                    <div class="rule-id">
                        {html.escape(rule_id)}
                        {severity_badge}
                    </div>
                    <div class="message">{html.escape(message)}</div>
                        '''
                        
                        # Adicionar localizações (apenas as válidas)
                        if 'locations' in result:
                            for location in result['locations']:
                                if 'physicalLocation' in location:
                                    artifact_location = location['physicalLocation'].get('artifactLocation', {})
                                    uri = artifact_location.get('uri', '')
                                    
                                    # Só mostrar localizações que não são do arquivo SARIF
                                    if not uri.endswith('.sarif'):
                                        region = location['physicalLocation'].get('region', {})
                                        start_line = region.get('startLine', 'N/A')
                                        
                                        html_content += f'''
                    <div class="location">
                        📁 {html.escape(uri)} | 📍 Linha {start_line}
                    </div>
                                        '''
                                        break  # Usar apenas a primeira localização válida
                        
                        html_content += '</div>'
            else:
                html_content += '''
            <div class="no-issues">
                <h2>🎉 Parabéns!</h2>
                <p>Nenhum problema de segurança foi encontrado na análise.</p>
            </div>
                '''
    else:
        html_content += '''
        <div class="no-issues">
            <h2>⚠️ Sem Resultados</h2>
            <p>Não foi possível processar os resultados da análise.</p>
        </div>
        '''
    
    html_content += '''
        </div>
    </div>
</body>
</html>'''
    
    # Salvar o HTML
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Relatório HTML gerado com sucesso: {output_file_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar relatório HTML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Usar argumentos da linha de comando ou valores padrão
    sarif_file = sys.argv[1] if len(sys.argv) > 1 else "semgrep-results.sarif"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "semgrep-report.html"
    
    generate_html_report(sarif_file, output_file) 