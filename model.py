import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from utils import Jsonable

db = SQLAlchemy()

class Task(db.Model, Jsonable):
    """ Represent a task in a todo-list """

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    task = db.Column(db.String)
    done = db.Column(db.Boolean, default=False)


class Word(db.Model):
    """ Represent a task in a todo-list """

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
