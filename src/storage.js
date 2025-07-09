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
}

export default new StorageManager(); 