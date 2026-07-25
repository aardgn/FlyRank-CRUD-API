import sqlite3
def get_connection():
    return sqlite3.connect("tasks.db")
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Buy milk", 0))
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Walk the dog", 0))
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Finish homework", 0))
    conn.commit()
    cur.close()
    conn.close()

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for row in rows:
        result.append({"id": row[0], "title": row[1], "done": row[2]})
    return result

def get_by_id(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return None
    else:
        return {"id": row[0], "title": row[1], "done": row[2]}

def create(title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False))
    new_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "title": title, "done": False}

def update(task_id, title, done):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
    row = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if row == 0:
        return None
    else:
        return {"id": task_id, "title": title, "done": done}

def delete(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE id = ?", (task_id,)
    )
    row = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if row == 0:
        return False
    else:
        return True