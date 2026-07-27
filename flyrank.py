from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import repository_sqlite as repository
from supabase_client import supabase
from fastapi import Header
from fastapi import Depends

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

def get_current_user(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    token = authorization.replace("Bearer ", "")
    try:
        result = supabase.auth.get_user(token)
        return result.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

@app.get("/protected/profile")
def protected_profile(user = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "created_at": user.created_at}

@app.post("/auth/logout", status_code=204)
def logout(user = Depends(get_current_user)):
    supabase.auth.sign_out()
    return Response(status_code=204)

@app.get("/protected/dashboard")
def protected_dashboard(user = Depends(get_current_user)):
    return {"message": "Welcome to your dashboard, {user.email}"}