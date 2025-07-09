# Prova de Conceito: Ofuscação e Deploy com Docker

Este repositório contém uma prova de conceito (PoC) para demonstrar um fluxo completo de CI/CD, incluindo:
1.  Ofuscação de múltiplos arquivos JavaScript.
2.  Containerização da aplicação com Docker (Nginx).
3.  Publicação da imagem Docker no **Docker Hub** via GitHub Actions.

## Estrutura do Projeto

```
/
├── .github/
│   └── workflows/
│       └── main.yml      // Workflow para build e push da imagem Docker
├── dist/                 // Diretório de output da ofuscação (gerado no build)
├── src/                  // Código JavaScript original
├── .dockerignore         // Ignora arquivos no build do Docker
├── config.json           // Configurações da ofuscação
├── Dockerfile            // Define a imagem Docker da aplicação
├── index.html            // Página principal da aplicação
├── package.json          // Dependências e scripts do projeto
└── README.md             // Este arquivo
```

## Fluxo de Trabalho de CI/CD

1.  **Configuração:** Antes de mais nada, é preciso configurar os secrets `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN` nas configurações do repositório no GitHub.
2.  **Desenvolvimento:** O código é desenvolvido localmente na pasta `src/`.
3.  **Commit/Push:** As alterações são enviadas para a branch `main` no GitHub.
4.  **GitHub Actions:** Um workflow é acionado para:
    *   Fazer login no Docker Hub usando os secrets.
    *   Construir a imagem Docker usando o `Dockerfile`.
    *   Enviar a imagem final para o Docker Hub com as tags `latest` e a do commit.

## Como Executar Localmente

### Pré-requisitos
-   [Node.js](https://nodejs.org/) e npm
-   [Docker](https://www.docker.com/products/docker-desktop/)

### 1. Construir e Rodar o Container
O `Dockerfile` automatiza todo o processo de instalação e build.

```bash
# 1. Construa a imagem Docker
docker build -t obfuscator-poc .

# 2. Execute o container a partir da imagem
docker run -d -p 8080:80 obfuscator-poc
```
Após isso, a aplicação estará disponível em **`http://localhost:8080`**.

## Deploy em Produção

Com a imagem publicada no Docker Hub, o deploy consiste em instruir um servidor a usar a nova imagem.

Um exemplo de fluxo de deploy manual em um servidor com Docker seria:

```bash
# (Substitua 'seu-usuario-docker' pelo seu username no Docker Hub)

# 1. Parar o container antigo
docker stop obfuscator-poc-container || true && docker rm obfuscator-poc-container || true

# 2. Baixar a imagem mais recente do Docker Hub
docker pull seu-usuario-docker/obfuscator-poc:latest

# 3. Iniciar o novo container
docker run -d --name obfuscator-poc-container -p 80:80 seu-usuario-docker/obfuscator-poc:latest
```
Este processo pode ser automatizado no workflow do GitHub Actions adicionando um job de deploy que se conecta ao servidor via SSH e executa esses comandos. 