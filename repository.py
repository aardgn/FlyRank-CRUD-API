import os 
import psycopg2
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


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
    cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
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
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;", (title, False)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": row[0], "title": row[1], "done": row[2]}

def update(task_id, title, done):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;", (title, done, task_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row is None:
        return None
    else:
        return {"id": row[0], "title": row[1], "done": row[2]}

def delete(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE id = %s;", (task_id,)
    )
    row = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if row == 0:
        return False
    else:
        return True