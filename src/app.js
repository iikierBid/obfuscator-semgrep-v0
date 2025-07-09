import './ui.js';

// VULNERABILIDADE INTENCIONAL PARA TESTE DE PIPELINE
// Esta chave de API deve ser detectada pelo Semgrep e bloquear o build.
const DANGEROUS_API_KEY = "sk_live_1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b";

// O arquivo ui.js já inicializa a aplicação
// Este arquivo serve apenas como ponto de entrada
console.log('Aplicação Todo List iniciada!'); 