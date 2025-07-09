import todoManager from './todoManager.js';

class UI {
    constructor() {
        this.todoList = document.getElementById('todoList');
        this.todoInput = document.getElementById('todoInput');
        this.addButton = document.getElementById('addButton');
        this.clearCompletedButton = document.getElementById('clearCompleted');
        this.filterButtons = document.querySelectorAll('.filter-button');
        
        this.initializeEventListeners();
        this.renderTodos();
    }

    initializeEventListeners() {
        this.addButton.addEventListener('click', () => this.handleAddTodo());
        this.todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleAddTodo();
        });
        this.clearCompletedButton.addEventListener('click', () => this.handleClearCompleted());
        this.filterButtons.forEach(button => {
            button.addEventListener('click', (e) => this.handleFilter(e.target.dataset.filter));
        });
    }

    handleAddTodo() {
        const text = this.todoInput.value.trim();
        if (text) {
            todoManager.addTodo(text);
            this.todoInput.value = '';
            this.renderTodos();
        }
    }

    handleClearCompleted() {
        todoManager.clearCompleted();
        this.renderTodos();
    }

    handleFilter(filter) {
        this.filterButtons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        this.renderTodos(filter);
    }

    createTodoElement(todo) {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        li.dataset.id = todo.id;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = todo.completed;
        checkbox.addEventListener('change', () => {
            todoManager.toggleTodo(todo.id);
            this.renderTodos();
        });

        const span = document.createElement('span');
        span.textContent = todo.text;
        span.addEventListener('dblclick', () => this.handleEdit(todo.id));

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '×';
        deleteButton.className = 'delete-button';
        deleteButton.addEventListener('click', () => {
            todoManager.removeTodo(todo.id);
            this.renderTodos();
        });

        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(deleteButton);
        return li;
    }

    handleEdit(id) {
        const todo = todoManager.getTodos().find(t => t.id === id);
        if (!todo) return;

        const li = this.todoList.querySelector(`[data-id="${id}"]`);
        const span = li.querySelector('span');
        const input = document.createElement('input');
        input.type = 'text';
        input.value = todo.text;
        input.className = 'edit-input';

        const saveEdit = () => {
            const newText = input.value.trim();
            if (newText) {
                todoManager.updateTodo(id, newText);
                this.renderTodos();
            }
        };

        input.addEventListener('blur', saveEdit);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') saveEdit();
        });

        span.replaceWith(input);
        input.focus();
    }

    renderTodos(filter = 'all') {
        this.todoList.innerHTML = '';
        let todos;

        switch (filter) {
            case 'active':
                todos = todoManager.getPendingTodos();
                break;
            case 'completed':
                todos = todoManager.getCompletedTodos();
                break;
            default:
                todos = todoManager.getTodos();
        }

        todos.forEach(todo => {
            this.todoList.appendChild(this.createTodoElement(todo));
        });
    }
}

export default new UI(); 