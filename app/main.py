from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI()


class TodoIn(BaseModel):
    title: str
    body: str


class Todo(TodoIn):
    id: int


todos: list[Todo] = []
current_id = 0


INDEX_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Todo App</title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
  <div id='app'>
    <h1>Todos</h1>
    <div>
      <input v-model='newTitle' placeholder='Title' />
      <input v-model='newBody' placeholder='Body' />
      <button @click='addTodo'>Add Todo</button>
    </div>
    <div v-for='todo in todos' :key='todo.id' style='border:1px solid #ccc; margin:5px; padding:5px;'>
      <input v-model='todo.title' @change='updateTodo(todo)' />
      <textarea v-model='todo.body' @change='updateTodo(todo)'></textarea>
      <button @click='deleteTodo(todo.id)'>Delete</button>
    </div>
  </div>
  <script>
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
          fetch('/api/todos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: this.newTitle, body: this.newBody }) })
            .then(r => r.json())
            .then(todo => { this.todos.push(todo); this.newTitle = ''; this.newBody = ''; });
        },
        updateTodo(todo) {
          fetch('/api/todos/' + todo.id, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: todo.title, body: todo.body }) });
        },
        deleteTodo(id) {
          fetch('/api/todos/' + id, { method: 'DELETE' }).then(r => { if (r.ok) { this.todos = this.todos.filter(t => t.id !== id); } });
        }
      },
      mounted() {
        this.fetchTodos();
      }
    }).mount('#app');
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_HTML


@app.get("/api/todos", response_model=list[Todo])
async def get_todos():
    return todos


@app.post("/api/todos", response_model=Todo)
async def create_todo(todo: TodoIn):
    global current_id
    current_id += 1
    item = Todo(id=current_id, **todo.dict())
    todos.append(item)
    return item


@app.put("/api/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoIn):
    for idx, item in enumerate(todos):
        if item.id == todo_id:
            updated = Todo(id=todo_id, **todo.dict())
            todos[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail='Todo not found')


@app.delete("/api/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    for idx, item in enumerate(todos):
        if item.id == todo_id:
            todos.pop(idx)
            return
    raise HTTPException(status_code=404, detail='Todo not found')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

