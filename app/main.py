from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class TodoIn(BaseModel):
    title: str
    body: str


class Todo(TodoIn):
    id: int


todos: list[Todo] = []
current_id = 0


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "templates/index.html")


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

