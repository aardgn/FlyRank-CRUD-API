from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import repository_sqlite as repository
app = FastAPI()
repository.init_db()

class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool
@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
#Stage2 checkpoint completed
@app.get("/tasks")
def get_all_tasks():
    return repository.get_all()
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    task = repository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return task

@app.post("/tasks", status_code=201)
def task_create(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    return repository.create(task.title)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
        if not task.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        new = repository.update(task_id, task.title, task.done)
        if new is None:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            return new
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    erase = repository.delete(task_id)
    if erase is False:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return Response(status_code=204)

# Stage5  Swagger UI completed