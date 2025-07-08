class StorageManager {
    constructor() {
        this.storageKey = 'todoList';
    }

    saveTodos(todos) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(todos));
            return true;
        } catch (error) {
            console.error('Erro ao salvar todos:', error);
            return false;
        }
    }

    loadTodos() {
        try {
            const todos = localStorage.getItem(this.storageKey);
            return todos ? JSON.parse(todos) : [];
        } catch (error) {
            console.error('Erro ao carregar todos:', error);
            return [];
        }
    }

    clearTodos() {
        try {
            localStorage.removeItem(this.storageKey);
            return true;
        } catch (error) {
            console.error('Erro ao limpar todos:', error);
            return false;
        }
    }

    // VULNERABILIDADE 4: SQL Injection
    // Função simulada para buscar um usuário no banco de dados
    findUserUnsafe(userInput) {
        // A construção da query via concatenação de string é insegura
        const query = "SELECT * FROM users WHERE username = '" + userInput + "';";
        console.log(`Executando query insegura: ${query}`);
        // Em um app real, aqui haveria uma chamada ao banco de dados: db.query(query);
        return { "id": 1, "username": "dummy_user" };
    }

    // VULNERABILIDADE MEDIUM: Uso de algoritmo de hash fraco
    // Função para criar um hash de dados, mas usando MD5 que é inseguro
    hashDataUnsafe(data) {
        // O uso de MD5 é considerado uma prática de segurança ruim
        const hash = md5(data); // Regra: javascript.lang.security.weak-hash.weak-hash
        console.log(`Hash MD5 gerado: ${hash}`);
        return hash;
    }
}

export default new StorageManager(); 