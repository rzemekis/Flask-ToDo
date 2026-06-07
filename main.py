import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка пути к базе данных
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
app.config['TRACK_MODIFICATIONS'] = False

# Инициализируем SQLAlchemy
db = SQLAlchemy(app)


#*-----*МОДЕЛЬ ДАННЫХ*-----*
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Task {self.title}>"


# *-----*МАРШРУТЫ*-----*

@app.route("/")
def index():
    # Выбор только активных задач
    tasks = Task.query.filter_by(active=1).all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    """Добавление новой задачи в БД"""
    title = request.form.get("title")
    if title and title.strip():
        new_task = Task(title=title.strip())
        db.session.add(new_task)
        db.session.commit()
    return redirect("/")


@app.route("/complete")
def complete_task():
    """Изменение статуса выполнения"""
    task_id = request.args.get("id")
    if task_id:
        task = Task.query.get(task_id)
        if task:
            task.completed = 1 - task.completed
            db.session.commit()
    return redirect("/")


@app.route("/delete")
def delete_task():
    """SAFE-удаления задачи (active=0)"""
    task_id = request.args.get("id")
    if task_id:
        task = db.session.get(Task, task_id)
        if task:
            task.active = 0
            db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    # Создаём БД в контексте приложения если ее нету
    with app.app_context():
        db.create_all()

    app.run(debug=True)