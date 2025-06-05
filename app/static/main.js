const { createApp } = Vue;
createApp({
  data() {
    return { todos: [], newTitle: '', newBody: '' };
  },
  methods: {
    fetchTodos() {
      fetch('/api/todos').then(r => r.json()).then(data => { this.todos = data; });
    },
    addTodo() {
      fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: this.newTitle, body: this.newBody })
      })
        .then(r => r.json())
        .then(todo => { this.todos.push(todo); this.newTitle = ''; this.newBody = ''; });
    },
    updateTodo(todo) {
      fetch('/api/todos/' + todo.id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: todo.title, body: todo.body })
      });
    },
    deleteTodo(id) {
      fetch('/api/todos/' + id, { method: 'DELETE' })
        .then(r => { if (r.ok) { this.todos = this.todos.filter(t => t.id !== id); } });
    }
  },
  mounted() {
    this.fetchTodos();
  }
}).mount('#app');
