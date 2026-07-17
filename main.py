from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
app = FastAPI()
task_db = []
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool
@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/task"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
#Stage2 checkpoint completed
@app.get("/tasks")
def get_all_tasks():
    return task_db
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    for task in task_db:
        if task["id"] == task_id:
            return task
        raise HTTPException(status_code=404, detail="Task not found")
@app.post("/tasks", status_code=201)
def task_create(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_id = max(t["id"] for t in task_db) + 1 if task_db else 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }
    task_db.append(new_task)
    return new_task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
        if not task.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        for t in task_db:
            if t["id"] == task_id:
                t["title"] = task.title
                t["done"] = task.done
                return t
        raise HTTPException(status_code=404, detail="Task not found")
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, t in enumerate(task_db):
        if t["id"] == task_id:
            task_db.pop(index)
            return Response(status_code=204)
        raise HTTPException(status_code=404, detail="Task not found")
# Stage5 completed
