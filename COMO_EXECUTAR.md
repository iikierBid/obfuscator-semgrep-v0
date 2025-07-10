# 🚀 Guia Rápido - Como Executar os Testes

## ⚡ **Execução Rápida (Pipeline)**

### **GitHub Actions (Automático)**
```bash
# O pipeline executa automaticamente em:
# - Push para qualquer branch
# - Pull requests
# - Acesso aos resultados via Actions tab
```

## 🖥️ **Execução Local**

### **1. Pré-requisitos**
```bash
# Instalar Semgrep via pip
pip install semgrep

# OU via Docker
docker pull returntocorp/semgrep
```

### **2. Execução Manual (Semgrep)**
```bash
# Comando completo
semgrep --config p/default --config p/trailofbits --config .semgrep.yml --sarif --output semgrep-results.sarif .

# Gerar relatório HTML
python scripts/generate_html_report.py semgrep-results.sarif relatorio.html
```

### **3. Execução Automatizada (Recomendado)**
```bash
# Script completo com análise detalhada
python scripts/test_vulnerabilities.py
```

### **4. Via Docker (Se preferir)**
```bash
# Executar Semgrep via Docker
docker run --rm -v $(pwd):/src returntocorp/semgrep --config p/default --config p/trailofbits --config .semgrep.yml --sarif --output /src/semgrep-results.sarif /src

# Gerar relatório
python scripts/generate_html_report.py semgrep-results.sarif relatorio.html
```

## 📊 **Arquivos de Saída**

Após execução, você terá:
- ✅ `semgrep-results.sarif` - Resultados em formato SARIF
- ✅ `relatorio.html` - Relatório visual HTML
- ✅ Logs detalhados no terminal

## 🎯 **Resultados Esperados**

**Total esperado: 70+ vulnerabilidades detectadas**

### **Por Categoria:**
- 💉 Injection: 15-20 vulnerabilidades
- 🕷️ XSS: 4-6 vulnerabilidades  
- 🔐 Crypto: 10-15 vulnerabilidades
- 🔑 Credentials: 20-25 vulnerabilidades
- 📁 Path Traversal: 3-5 vulnerabilidades
- 💥 Dangerous Functions: 5-8 vulnerabilidades
- 🔄 Outras: 10-15 vulnerabilidades

## 🔧 **Resolução de Problemas**

### **Semgrep não encontrado**
```bash
# Verificar instalação
semgrep --version

# Reinstalar se necessário
pip install --upgrade semgrep
```

### **Erro de Python**
```bash
# Verificar Python 3.6+
python --version

# Executar com caminho completo se necessário
python3 scripts/test_vulnerabilities.py
```

### **Permissões no Docker**
```bash
# Linux/Mac - ajustar permissões
sudo chown -R $USER:$USER .

# Windows - executar PowerShell como Admin
```

## 📈 **Interpretação dos Resultados**

### **Exit Codes:**
- `0` - Nenhuma vulnerabilidade (inesperado neste projeto)
- `1` - Vulnerabilidades encontradas (sucesso!)
- `2` - Erro na execução

### **Severidades:**
- 🔴 **ERROR** - Vulnerabilidades críticas
- 🟡 **WARNING** - Problemas importantes
- 🔵 **INFO** - Informações gerais

## 🎓 **Próximos Passos**

Após executar os testes:

1. **📋 Analise o relatório HTML** para entender as vulnerabilidades
2. **🔍 Revise o código** para ver os exemplos práticos
3. **📚 Consulte a documentação** para aprofundamento
4. **🔧 Experimente customizar** as regras do Semgrep

---

**🏆 Sucesso! Você agora tem uma bateria completa de testes de vulnerabilidades rodando!** 