from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Инициализация без привязки к конкретному приложению

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Task {self.title}>"