#!/usr/bin/env python3
"""
🔒 SEMGREP VULNERABILITY TEST SUITE
===================================
Script automatizado para testar vulnerabilidades de segurança usando Semgrep.
Este projeto é UNIVERSALMENTE REUTILIZÁVEL em qualquer linguagem de programação.

Linguagens suportadas:
- JavaScript, TypeScript, Python, Java, Kotlin
- C#, Go, PHP, Ruby, Swift, Scala, Rust, Dart
- C/C++, YAML, JSON, XML, TOML, Properties

Uso:
    python scripts/test_vulnerabilities.py

Autor: Assistant - Projeto POC Semgrep
Data: 2024
"""

import subprocess
import sys
import json
import os
from pathlib import Path
from datetime import datetime

def print_header():
    """Imprime o cabeçalho do script"""
    print("🔒 SEMGREP VULNERABILITY TEST SUITE")
    print("="*50)
    print("🌍 PROJETO UNIVERSAL - SUPORTA TODAS AS LINGUAGENS")
    print("="*50)
    print(f"📅 Executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def print_supported_languages():
    """Mostra as linguagens suportadas"""
    print("🌐 LINGUAGENS SUPORTADAS:")
    print("="*30)
    
    languages = {
        "Web & Mobile": ["JavaScript", "TypeScript", "Dart", "Swift"],
        "Backend": ["Python", "Java", "Kotlin", "C#", "Go", "PHP", "Ruby", "Scala"],
        "Systems": ["C", "C++", "Rust"],
        "Config": ["YAML", "JSON", "XML", "TOML", "Properties"]
    }
    
    for category, langs in languages.items():
        print(f"  {category}:")
        for lang in langs:
            print(f"    ✓ {lang}")
    
    print()
    print("💡 Este projeto detecta vulnerabilidades em QUALQUER uma dessas linguagens!")
    print("🔄 Totalmente reutilizável em projetos diferentes!")
    print()

def run_semgrep():
    """Executa o Semgrep com configurações abrangentes"""
    print("🚀 EXECUTANDO SEMGREP...")
    print("="*30)
    
    # Comando Semgrep com múltiplas fontes de regras
    cmd = [
        "semgrep",
        "--config", "p/default",        # Regras padrão do Semgrep
        "--config", "p/trailofbits",    # Regras Trail of Bits
        "--config", "p/r2c-security-audit",  # Regras R2C Security
        "--config", ".semgrep.yml",     # Regras customizadas universais
        "--sarif",                      # Formato SARIF
        "--output", "semgrep-results.sarif",
        "--verbose",
        "."
    ]
    
    print(f"📋 Comando executado: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        print("📊 RESULTADO DA EXECUÇÃO:")
        print(f"   Return Code: {result.returncode}")
        print(f"   STDOUT: {result.stdout}")
        if result.stderr:
            print(f"   STDERR: {result.stderr}")
        
        return result.returncode == 0 or result.returncode == 1  # 1 = vulnerabilidades encontradas
        
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: Semgrep demorou mais de 5 minutos!")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def analyze_results():
    """Analisa os resultados do arquivo SARIF"""
    sarif_file = "semgrep-results.sarif"
    
    if not os.path.exists(sarif_file):
        print("❌ Arquivo SARIF não encontrado!")
        return
    
    print("📊 ANÁLISE DE RESULTADOS:")
    print("="*30)
    
    try:
        with open(sarif_file, 'r', encoding='utf-8') as f:
            sarif_data = json.load(f)
        
        # Extrair estatísticas
        runs = sarif_data.get('runs', [])
        total_results = 0
        rules_count = 0
        files_affected = set()
        
        for run in runs:
            results = run.get('results', [])
            total_results += len(results)
            
            # Contar regras
            tool_rules = run.get('tool', {}).get('driver', {}).get('rules', [])
            rules_count += len(tool_rules)
            
            # Arquivos afetados
            for result in results:
                locations = result.get('locations', [])
                for location in locations:
                    uri = location.get('physicalLocation', {}).get('artifactLocation', {}).get('uri', '')
                    if uri:
                        files_affected.add(uri)
        
        print(f"🔍 Total de vulnerabilidades encontradas: {total_results}")
        print(f"📋 Total de regras aplicadas: {rules_count}")
        print(f"📁 Arquivos com vulnerabilidades: {len(files_affected)}")
        print()
        
        # Mostrar arquivos afetados
        if files_affected:
            print("📁 ARQUIVOS AFETADOS:")
            for file in sorted(files_affected):
                print(f"   • {file}")
        
        print()
        print("🎯 ANÁLISE POR CATEGORIA:")
        
        # Agrupar por regra
        rule_stats = {}
        for run in runs:
            results = run.get('results', [])
            for result in results:
                rule_id = result.get('ruleId', 'unknown')
                if rule_id not in rule_stats:
                    rule_stats[rule_id] = 0
                rule_stats[rule_id] += 1
        
        for rule_id, count in sorted(rule_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {rule_id}: {count} ocorrências")
        
        print()
        print("✅ PROJETO PRONTO PARA REUTILIZAÇÃO!")
        print("📋 Para usar em outros projetos:")
        print("   1. Copie o arquivo .semgrep.yml")
        print("   2. Execute: semgrep --config .semgrep.yml .")
        print("   3. O projeto detectará vulnerabilidades em qualquer linguagem!")
        
    except Exception as e:
        print(f"❌ Erro ao analisar resultados: {e}")

def generate_html_report():
    """Gera relatório HTML usando o script Python"""
    print("📄 GERANDO RELATÓRIO HTML...")
    print("="*30)
    
    try:
        cmd = [sys.executable, "scripts/generate_html_report.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Relatório HTML gerado com sucesso!")
            print("📄 Arquivo: semgrep-report.html")
        else:
            print(f"❌ Erro ao gerar relatório HTML: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print_header()
    print_supported_languages()
    
    print("🔧 VERIFICANDO DEPENDÊNCIAS...")
    
    # Verificar se o Semgrep está instalado
    try:
        result = subprocess.run(["semgrep", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Semgrep encontrado: {result.stdout.strip()}")
        else:
            print("❌ Semgrep não encontrado! Instale com: pip install semgrep")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ Semgrep não encontrado! Instale com: pip install semgrep")
        sys.exit(1)
    
    print()
    
    # Executar Semgrep
    if run_semgrep():
        print("✅ Semgrep executado com sucesso!")
        print()
        
        # Analisar resultados
        analyze_results()
        
        # Gerar relatório HTML
        generate_html_report()
        
        print()
        print("🎉 TESTE COMPLETO FINALIZADO!")
        print("📊 Verifique os arquivos:")
        print("   • semgrep-results.sarif (resultados detalhados)")
        print("   • semgrep-report.html (relatório visual)")
        
    else:
        print("❌ Falha na execução do Semgrep!")
        sys.exit(1)

if __name__ == "__main__":
    main() 