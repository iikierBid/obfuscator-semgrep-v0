# Implementação SAST com Semgrep - Configuração Genérica

## 📋 Visão Geral

Esta implementação fornece uma configuração **genérica e reutilizável** do Semgrep para análise de segurança estática (SAST) que pode ser aplicada em múltiplos projetos com diferentes linguagens de programação.

## 🎯 Características Principais

### ✅ Metodologia Trunk-Based Development
- **Scans no push para `main`**: Garantem que o código principal está sempre seguro
- **Scans em Pull Requests**: Identificam vulnerabilidades antes do merge
- **Comparação com branch principal**: Analisa apenas as mudanças introduzidas
- **Feedback imediato**: Comentários automáticos em PRs com resultados

### ✅ Configuração Genérica
- **Auto-detecção de linguagens**: Funciona com JavaScript, Python, Java, Go, C#, etc.
- **Rulesets universais**: Focados em vulnerabilidades comuns (OWASP Top 10, CWE-25)
- **Facilmente adaptável**: Pode ser customizado para projetos específicos

### ✅ Integração com GitHub
- **GitHub Security Tab**: Resultados integrados à interface do GitHub
- **Relatórios SARIF**: Padrão da indústria para análise de segurança
- **Aprovação obrigatória**: Deploy só acontece após análise de segurança

## 🏗️ Arquitetura da Solução

### Por que esta abordagem?

**1. Segurança Shift-Left**
- Identifica vulnerabilidades no início do ciclo de desenvolvimento
- Reduz custos de correção (bugs encontrados em produção custam 100x mais)
- Melhora a qualidade geral do código

**2. Automação DevSecOps**
- Elimina análises manuais propensas a erro
- Garante consistência entre projetos
- Libera desenvolvedores para focar em funcionalidades

**3. Compliance e Auditoria**
- Histórico completo de análises no GitHub
- Rastreabilidade de vulnerabilidades
- Evidências para auditorias de segurança

## 🚀 Configuração por Projeto

### Configuração Básica (Funciona para qualquer linguagem)
```yaml
# .github/workflows/sast-semgrep.yml
config: >-
  p/security-audit    # Regras gerais de segurança
  p/owasp-top-ten    # OWASP Top 10
  p/cwe-top-25       # CWE Top 25
  auto               # Auto-detecção de linguagem
```

### Personalizações por Linguagem

#### JavaScript/Node.js
```yaml
config: >-
  p/security-audit
  p/owasp-top-ten
  p/javascript
  p/nodejs
  p/react        # Se usar React
  p/express      # Se usar Express
```

#### Python
```yaml
config: >-
  p/security-audit
  p/owasp-top-ten
  p/python
  p/django       # Se usar Django
  p/flask        # Se usar Flask
```

#### Java
```yaml
config: >-
  p/security-audit
  p/owasp-top-ten
  p/java
  p/spring       # Se usar Spring
```

#### Go
```yaml
config: >-
  p/security-audit
  p/owasp-top-ten
  p/golang
```

## 🔧 Implementação Passo a Passo

### 1. Copiar Arquivos Base
```bash
# Copie estes arquivos para seu projeto:
.github/workflows/sast-semgrep.yml   # Workflow principal
.semgrep.yml                         # Regras customizadas (opcional)
```

### 2. Configurar Secrets no GitHub

**Obrigatório:**
- `SEMGREP_APP_TOKEN`: Token do Semgrep Cloud (opcional, mas recomendado)
  - Acesse: https://semgrep.dev/manage/settings/tokens
  - Crie um token para seu projeto
  - Adicione em Settings > Secrets > Actions

**Por que usar Semgrep Cloud?**
- Análise mais rápida e precisa
- Menos falsos positivos
- Suporte a mais linguagens
- Histórico de análises

### 3. Personalizar para Sua Linguagem

Edite o arquivo `.github/workflows/sast-semgrep.yml`:

```yaml
config: >-
  p/security-audit
  p/owasp-top-ten
  p/cwe-top-25
  p/SUA_LINGUAGEM    # Substitua por: javascript, python, java, etc.
  auto
```

### 4. Testar a Configuração

```bash
# Teste local (opcional)
npm install -g @semgrep/cli
semgrep --config=p/security-audit --config=p/javascript .
```

## 🎯 Vulnerabilidades Detectadas

### Regras Genéricas (Todos os Projetos)

#### 1. Credenciais Hardcoded
```javascript
// ❌ Detectado
const password = "super_secret_123";
const apiKey = "sk-1234567890abcdef";

// ✅ Correto
const password = process.env.PASSWORD;
const apiKey = process.env.API_KEY;
```

#### 2. SQL Injection
```javascript
// ❌ Detectado
const query = "SELECT * FROM users WHERE id = " + userId;

// ✅ Correto  
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);
```

#### 3. Path Traversal
```javascript
// ❌ Detectado
const filePath = "/uploads/" + req.params.filename;

// ✅ Correto
const filePath = path.join("/uploads/", path.basename(req.params.filename));
```

### Regras Específicas por Linguagem

Cada linguagem tem regras específicas adicionais:
- **JavaScript**: XSS, Prototype Pollution, Weak Crypto
- **Python**: Command Injection, Deserialization
- **Java**: XXE, Insecure Deserialization
- **Go**: Race Conditions, Memory Leaks

## 📊 Métricas e Monitoramento

### GitHub Security Tab
- **Vulnerabilidades por severidade**: Critical, High, Medium, Low
- **Tendências**: Aumento/diminuição de vulnerabilidades
- **Tempo de resolução**: Tempo médio para correção

### Relatórios Automáticos
- **Comentários em PR**: Resumo executivo das vulnerabilidades
- **Bloqueio de merge**: PRs com vulnerabilidades críticas
- **Notificações**: Alertas automáticos para equipe de segurança

## 🔄 Fluxo de Trabalho

### Para Desenvolvedores
1. **Desenvolver**: Crie sua funcionalidade normalmente
2. **Commit**: Faça commit das alterações
3. **Push**: Envie para branch feature
4. **PR**: Abra Pull Request para `main`
5. **Aguardar**: Semgrep analisa automaticamente
6. **Corrigir**: Se houver vulnerabilidades, corrija antes do merge
7. **Merge**: Após aprovação, faça merge para `main`

### Para DevSecOps
1. **Configurar**: Implemente o workflow uma vez
2. **Monitorar**: Acompanhe métricas no GitHub Security
3. **Ajustar**: Refine regras conforme necessário
4. **Educar**: Treine equipe sobre vulnerabilidades comuns

## 🛡️ Boas Práticas de Segurança

### 1. Princípio da Defesa em Profundidade
- **SAST (Semgrep)**: Análise estática do código
- **DAST**: Testes dinâmicos em ambiente de teste
- **SCA**: Análise de dependências vulneráveis
- **IaC Security**: Segurança de infraestrutura como código

### 2. Shift-Left Security
- Encontre vulnerabilidades cedo no ciclo
- Treine desenvolvedores sobre segurança
- Automatize tudo que for possível
- Meça e melhore continuamente

### 3. Gestão de Vulnerabilidades
- **Priorize por risco**: Critical > High > Medium > Low
- **Defina SLAs**: Tempo máximo para correção
- **Documente exceções**: Justifique casos onde não é possível corrigir
- **Monitore tendências**: Estamos melhorando ou piorando?

## 🚨 Troubleshooting

### Problema: Muitos falsos positivos
**Solução**: Ajuste as regras no arquivo `.semgrep.yml`
```yaml
# Desabilitar regra específica
rules:
  - id: minha-regra-customizada
    pattern: ...
    severity: WARNING  # Reduzir severidade
```

### Problema: Análise muito lenta
**Solução**: 
1. Use Semgrep Cloud (mais rápido)
2. Limite análise a arquivos alterados
3. Exclude diretórios desnecessários

### Problema: Workflow não roda
**Solução**: Verifique permissões do token
```yaml
permissions:
  security-events: write
  contents: read
  pull-requests: write
```

## 📚 Recursos Adicionais

### Documentação
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/Top10/)

### Ferramentas Complementares
- **Dependabot**: Atualização automática de dependências
- **CodeQL**: Análise de segurança nativa do GitHub
- **Snyk**: Análise de dependências vulneráveis
- **SonarQube**: Análise de qualidade e segurança

### Treinamento
- [Secure Code Warrior](https://www.securecodewarrior.com/)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [Damn Vulnerable Web Application](https://dvwa.co.uk/)

---

## 🎉 Conclusão

Esta implementação genérica do Semgrep oferece:

✅ **Segurança desde o início** - Shift-left security  
✅ **Automação completa** - Zero intervenção manual  
✅ **Escalabilidade** - Funciona para qualquer linguagem  
✅ **Compliance** - Atende regulamentações de segurança  
✅ **ROI comprovado** - Reduz custos de correção de bugs  

**Próximos passos:**
1. Implemente em um projeto piloto
2. Monitore métricas por 30 dias
3. Ajuste regras conforme necessário
4. Expanda para outros projetos
5. Integre com outras ferramentas de segurança

*"A segurança não é um produto, é um processo"* - Bruce Schneier 