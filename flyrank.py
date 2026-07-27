from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import repository_sqlite as repository
from supabase_client import supabase
from fastapi import Header

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

class AuthRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=201)
def signup(auth: AuthRequest):
    if not auth.email.strip() or not auth.password.strip():
        raise HTTPException(status_code=400, detail="Email and password required.")
    result = supabase.auth.sign_up({"email": auth.email, "password": auth.password})
    return result.user

@app.post("/auth/login")
def login(auth: AuthRequest):
    if not auth.email.strip() or not auth.password.strip():
        raise HTTPException(status_code=400, detail="Email and password required.")
    try:
        result = supabase.auth.sign_in_with_password({"email": auth.email, "password": auth.password})
        return {"access_token": result.session.access_token, "refresh_token": result.session.refresh_token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required.")
    token = authorization.replace("Bearer ", "")
    try:
        result = supabase.auth.get_user(token)
        return {"id": result.user.id, "email": result.user.email, "created_at": result.user.created_at}
    except Exception as e:
        print(f"HATA: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")