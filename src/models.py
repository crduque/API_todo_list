from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    tasks_relationship = db.relationship("Tasks", lazy = True)

    def __repr__(self):
        return f"User: {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }
    
    @classmethod
    def get_user(cls, username):
        user = User.query.filter_by(username = username).first() # devuelve el primero que encuentra
        return user.serialize()

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    # def delete_user(username):
    #     user = User.query.filter_by(username = username).first()
    #     db.session.remove(user)
    #     db.session.commit()

class Tasks(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(120), ForeignKey("user.username"))
    task_text = db.Column(db.String(250))
    task_done = db.Column(db.Boolean(False))

    def __repr__(self):
        return f"task: {self.task_text}, done: {self.task_done}"

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "task_text": self.task_text,
            "task_done": self.task_done
        }

    def add_task(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_tasks(cls, username):
        tasks = Tasks.query.filter_by(user_name = username)
        all_tasks = list(map(lambda x: x.serialize(), tasks))
        return all_tasks

    def update_task(self, username, task_id, task_text, task_done):
        task = Tasks.query.filter_by(user_name = username, id=task_id).first()
        task.task_text = task_text
        task.task_done = task_done
        db.session.commit()
        return task
