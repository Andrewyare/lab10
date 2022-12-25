from .. import db
from datetime import datetime
import enum

class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Progress(enum.Enum):
    TODO = 1
    DOING = 2
    DONE = 3

task_user = db.Table('task_user',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                     )

class Task(db.Model):
	__tablename__ = "task"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(120), nullable=False)
	description = db.Column(db.String(2000), nullable=True)
	created = db.Column(db.DateTime, default=datetime.now())
	modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
	deadline = db.Column(db.DateTime)
	priority = db.Column(db.Enum(Priority, values_callable=lambda x: [str(member.value) for member in Priority]))
	progress = db.Column(db.Enum(Progress, values_callable=lambda x: [str(member.value) for member in Progress]))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

	users = db.relationship('User', secondary=task_user, backref=db.backref('tasks', lazy='dynamic'), lazy='dynamic')

	def __repr__(self):
	    return f"Title: {self.title}"
		
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    tasks = db.relationship('Task', backref='category', lazy='dynamic')