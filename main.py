import os
from flask import Flask, render_template, request, redirect
from models import db, Task

app = Flask(__name__)

# Пути
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
app.config['TRACK_MODIFICATIONS'] = False

# Связи бд с приложением
db.init_app(app)

# Авто-создание таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    # Достаем ток те задачи что active=1 (не active=0)
    tasks = Task.query.filter_by(active=1).all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    """Добавление новой задачи"""
    title = request.form.get("title")
    if title and title.strip():
        new_task = Task(title=title.strip())
        db.session.add(new_task)
        db.session.commit()
    return redirect("/")

@app.route("/complete")
def complete_task():
    """Переключение статуса выполнения"""
    task_id = request.args.get("id")
    if task_id:
        task = Task.query.get(task_id)
        if task:
            task.completed = 1 - task.completed
            db.session.commit()
    return redirect("/")

@app.route("/delete")
def delete_task():
    """Безопасное eдаление задачи (active=0)"""
    task_id = request.args.get("id")
    if task_id:
        task = db.session.get(Task, task_id)
        if task:
            task.active = 0
            db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)