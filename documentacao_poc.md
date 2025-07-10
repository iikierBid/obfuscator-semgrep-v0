# Documentação: Prova de Conceito de Ofuscação de Código

## 1. Ferramenta de Ofuscação Utilizada: `javascript-obfuscator`

A ferramenta selecionada para esta prova de conceito foi o **`javascript-obfuscator`**. É uma poderosa biblioteca de código aberto para Node.js que ofusca o código JavaScript, tornando-o extremamente difícil de ler e entender.

**Principais Vantagens:**
-   **Gratuita e de Código Aberto:** Não possui custos de licenciamento.
-   **Altamente Configurável:** Oferece dezenas de opções para ajustar o nível e o tipo de ofuscação.
-   **Integração com Ferramentas de Build:** Funciona bem com Webpack, Gulp, Grunt e scripts NPM, o que a torna ideal para automação em pipelines de CI/CD.
-   **Recursos Avançados:** Inclui mecanismos de autodefesa e proteção contra debug.

## 2. Configurações Básicas e Utilizadas

A ofuscação foi controlada pelo arquivo `config.json`. Abaixo estão detalhadas algumas das principais configurações que utilizamos e o que elas fazem:

-   `"compact": true`: Remove espaços em branco e quebras de linha, tornando o código mais compacto.
-   `"controlFlowFlattening": true`: Altera drasticamente a estrutura do código, escondendo a lógica original dentro de um loop `while` com um `switch`. É uma das técnicas mais eficazes para dificultar a análise.
-   `"deadCodeInjection": true`: Adiciona blocos de código aleatórios e inúteis no meio do código funcional para confundir quem tenta entendê-lo.
-   `"debugProtection": true`: Adiciona mecanismos que dificultam o uso de ferramentas de debug (como o DevTools do navegador). Por exemplo, pode inserir `debugger;` em intervalos, pausando a execução e atrapalhando a análise.
-   `"selfDefending": true`: Torna o código "autodefensivo". Se alguém tentar formatar ou embelezar o código para facilitar a leitura, ele pode parar de funcionar.
-   `"stringArray": true`: Remove todas as strings literais do código e as armazena em um array central. O código original é modificado para chamar essas strings a partir do array, geralmente através de uma função decodificadora.
-   `"stringArrayEncoding": ["base64"]`: Codifica as strings no `stringArray` usando Base64, adicionando uma camada extra de proteção.
-   `"transformObjectKeys": true`: Renomeia as chaves dos objetos.

## 3. O que a Ferramenta Pode Fazer (Capacidades)

-   **Proteger a Propriedade Intelectual:** Dificulta que concorrentes ou maus atores copiem, colem e reutilizem sua lógica de negócio e algoritmos do front-end.
-   **Dificultar a Engenharia Reversa:** Torna a análise do funcionamento da aplicação muito mais complexa e demorada.
-   **Esconder Endpoints e Chaves:** Ajuda a ocultar a forma como a aplicação se comunica com APIs, embora não substitua a segurança no back-end.
-   **Adicionar Camadas de Autoproteção:** Com opções como `selfDefending` e `debugProtection`, o código ativamente resiste a tentativas de análise.

## 4. Possíveis Impactos

A ofuscação é uma ferramenta poderosa, mas traz consigo alguns impactos que devem ser considerados:

-   **Impacto na Performance:** O código ofuscado pode ser um pouco mais lento para executar. Técnicas como `controlFlowFlattening` e `stringArray` introduzem mais passos e complexidade, o que pode aumentar o tempo de processamento. O impacto varia de acordo com a intensidade da ofuscação.
-   **Aumento no Tamanho do Arquivo:** O arquivo final ofuscado é significativamente maior que o original devido à adição de código (como em `deadCodeInjection`) e à complexidade das estruturas. No entanto, ele geralmente comprime muito bem com Gzip ou Brotli no servidor, minimizando o impacto no tempo de carregamento.
-   **Dificuldade de Debug:** É praticamente impossível depurar o código ofuscado em um ambiente de produção. Se um erro ocorrer, o *stack trace* será quase ininteligível.
    -   **Mitigação:** É crucial ter um sistema de monitoramento de erros (como Sentry, LogRocket, etc.) configurado para usar **Source Maps**. O `javascript-obfuscator` pode gerar source maps que traduzem os erros do código ofuscado de volta para o código original, mas isso deve ser feito com cuidado para não expor os mapas publicamente.
-   **Falsos Positivos de Antivírus:** Em casos raros, técnicas de ofuscação muito agressivas podem ser sinalizadas por alguns softwares de antivírus, que as confundem com características de malware.

## 5. Como Funciona via CI/CD

O fluxo de CI/CD que implementamos automatiza todo o processo, garantindo que o código-fonte permaneça legível no repositório e que apenas a versão ofuscada e pronta para produção seja distribuída.

O processo, definido em `.github/workflows/main.yml`, funciona da seguinte forma:

1.  **Gatilho (Trigger):** Qualquer `push` na branch `main` inicia o workflow.
2.  **Ambiente de Build:** O GitHub Actions prepara um ambiente virtual com Docker.
3.  **Login no Registry:** O workflow faz login de forma segura no **Docker Hub**, usando as credenciais armazenadas nos *Secrets* do GitHub (`DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`).
4.  **Build da Imagem Docker:**
    -   A construção da imagem ocorre em múltiplos estágios, conforme definido no `Dockerfile`.
    -   **Estágio de Build:** Uma imagem Node.js é usada para instalar as dependências (`npm ci`) e, crucialmente, executar o script de ofuscação (`npm run obfuscate`). Isso gera os arquivos ofuscados na pasta `/dist`.
    -   **Estágio Final:** Uma imagem leve do Nginx é usada como base. Apenas os arquivos de produção (`index.html` e a pasta `dist` ofuscada) são copiados do estágio anterior. O resultado é uma imagem final pequena e otimizada.
5.  **Push para o Registry:** A imagem Docker recém-construída é enviada para o Docker Hub, pronta para ser usada no ambiente de produção.
6.  **Deploy (Passo Final):** O trabalho do CI/CD termina ao publicar a imagem. A etapa final, que ocorre no ambiente de produção, é baixar (`pull`) essa nova imagem do Docker Hub e reiniciar o container da aplicação. Este passo pode ser manual ou automatizado com um job de deploy adicional. 