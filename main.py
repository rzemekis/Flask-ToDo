import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DB_NAME = "db.sqlite3"

def init_db():
    """Создание БД если ее нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1
            )
        ''')
    conn.commit()
    conn.close()

@app.route("/")
def index ():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, completed FROM tasks WHERE active = 1")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    """Добавка новой задачм в БД с использованием пост."""
    title = request.form.get("title")
    if title and title.strip():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, completed, active) VALUES (?, 0, 1)", (title.strip(),))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/complete")
def complete_task():
    """Измена статуса выоплнения"""
    task_id = request.args.get("id")
    if task_id:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = 1 - completed WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/delete")
def delete_task():
    """SAFE Удаление задачи(не удаление а active=0)"""
    task_id = request.args.get("id")
    if task_id:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET active = 0 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)