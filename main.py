from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
task_db = []
class TaskCreate(BaseModel):
    title: str
@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/task"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
#Stage2 checkpoint completed
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