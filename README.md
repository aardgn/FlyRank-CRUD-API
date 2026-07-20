# FlyRank Internship - To-Do CRUD API

This is a RESTful API that manages a to-do list built with Python and FastAPI. 
**Update (Stage A2):** The data storage has been migrated from an in-memory list to a persistent PostgreSQL database running in Docker.

## 🚀 How to Run (Docker)

The entire stack (the FastAPI application and the PostgreSQL database) is containerized.

1. Create your environment file from the provided example:
   ```bash
   cp .env.example .env
   ```
2. Start the application and database together:
   ```bash
   docker compose up -d
   ```
3. The API will be available at `http://localhost:8000`
4. Interactive Swagger UI is at `http://localhost:8000/docs`

## 🏗️ Architecture & Database Migration

* **Service and Routes Unchanged:** A new PostgreSQL repository (`repository.py`) was written to handle all SQL queries. It implements the exact same interface as the old in-memory store. Because of this clean separation, **the service and routes in `main.py` remained completely unchanged.**
* **Environment Variables:** The database connection string is securely loaded from the `.env` file (which is gitignored). A `.env.example` file is committed to the repo to show the expected format.

## 💾 Proof of Persistence

The PostgreSQL database runs inside a Docker container with a configured **named volume** (`pgdata`). Persistence was verified with the following steps:
1. Started the stack with `docker compose up -d`.
2. Created a new task via `POST /tasks`:
   ```bash
   curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Persistence Test"}'
   ```
3. Destroyed the running containers using `docker compose down`.
4. Restarted the stack with `docker compose up -d`.
5. Sent a `GET /tasks` request and confirmed the task was still there, proving the volume successfully persisted the data.

---

## Endpoints

| HTTP Method | Path | Description |
|---|---|---|
| GET | `/` | API Root info |
| GET | `/health` | Health Check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{task_id}` | Get single task |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}`| Delete a task |

## Example Request & Response

Creating a new task using curl:
```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

```http
HTTP/1.1 201 Created
date: Thu, 16 Jul 2026 17:52:41 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

![Swagger UI Screenshot](swagger.png)

---

## AI vs Me

### My Prompt

Using Python FastAPI: GET("/"), GET("/health"), GET("/tasks"), GET /tasks/{task_id}
returns 200 normally, but raises 404 if the task is not found (using HTTPException).
POST("/tasks", status_code=201). PUT /tasks/{task_id} returns 200 normally, raises 404
if the title is empty or if the task is not found. DELETE("/tasks/{task_id}",
status_code=204), raises 404 if the task is not found. No database — in-memory storage
only. Uses Swagger UI.

### What did the AI do better — and do I understand its version well enough to explain it?

The AI added a `response_model` parameter to every endpoint (e.g. `response_model=Task`,
`response_model=List[Task]`). This tells FastAPI exactly what shape each response must
have, and FastAPI validates the outgoing data against it automatically. In a small project
like this it isn't strictly necessary — my plain `dict` responses work fine — but in a
larger codebase or a team setting, `response_model` catches shape mismatches early and
makes the Swagger docs more precise. I understand why it's there and could explain it,
even though I didn't use it myself.

### What did it get wrong or quietly ignore from my prompt?

My prompt told it to return 404 when the title is empty in `PUT /tasks/{task_id}` — but
that's actually a request validation error, which should be 400, not 404 (400 means "the
data you sent is invalid," 404 means "the resource you're asking for doesn't exist"). I
made this mistake in my own prompt because I copied an earlier bug from my own code
without re-checking it. The AI didn't correct me — it implemented exactly what I asked
for, and even left a comment flagging it: `# Normally this would be a 400 Bad Request,
but implemented as 404 per your instructions`. It didn't push back or fix my mistake; it
just followed the specification as given, which is exactly the lesson this stage is
about — an AI's output is only as good as what you specify.

### What did my prompt forget to specify — and what did the AI silently decide for you?

I never mentioned `response_model`, `List`, or `Optional` at all — the AI added these on
its own. It also added a `description` field to the `Task` model that I never asked for,
and used a `dict` keyed by `task_id` (`tasks_db = {}`) instead of the list I used
(`task_db = []`). These are reasonable default decisions, but they were entirely the
AI's own choices, made silently because my prompt didn't constrain the internal data
structure — only the endpoints and status codes.

### One-sentence takeaway after the rematch

If I rewrote the prompt, I'd fix my own PUT/title status code mistake (400, not 404) and
explicitly state the data structure (a list vs a dict) so the AI's internal implementation
choices matched mine more closely.
