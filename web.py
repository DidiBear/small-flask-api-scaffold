import os
import sys
import logging 

from flask import Flask, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restless import APIManager
from flask_basicauth import BasicAuth

from utils import success, error
from model import db, Task, Word

DB_FILE = './database.db'
BASIC_AUTH = ("admin", "admin")

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = BASIC_AUTH[0]
app.config['BASIC_AUTH_PASSWORD'] = BASIC_AUTH[1]
app.config['BASIC_AUTH_FORCE'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + DB_FILE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'mysecretkey'

BasicAuth().init_app(app)
db.init_app(app)

# List of all model class
models = [Task, Word] # list(dict(inspect.getmembers(model, inspect.isclass)).values())

with app.app_context():
    # Create admin page     /admin
    admin = Admin(app)
    for model in models:
        admin.add_view(ModelView(model, db.session))

    # Create REST api       /api/<table>
    api_manager = APIManager(app, flask_sqlalchemy_db=db)
    for model in models:
        api_manager.create_api(model, methods=["GET", "POST", "PATCH", "DELETE"])

# Custom Behaviour

@app.route("/hello", defaults={"name": None})
@app.route("/hello/<name>")
def hello(name):
    if name: 
        return success(f"Hello {name} !" ), 200
    return error("You have to say your name : /hello/<name>"), 400

@app.route("/search_tasks/<search>")
def view_tasks(search):
    tasks = Task.query.filter(Task.task.like(f"%{search}%")).all()
    return success(data = tasks)


# Basic behaviour

@app.route("/")
def index():
    return redirect("/admin")

@app.errorhandler(500)
def internal_server_error(err):
    return error(str(err))

# MAIN

@app.before_first_request
def setup_logging():
    if not app.debug:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

def app_with_config(my_arg = None):
    """ Gunicorn entry point : $ gunicorn 'web:app_with_config(my_arg="value")'"""

    app.config["CONFIG_ARGS"] = my_arg
    return app

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Launch the web app in debug mode, use 'gunicorn web:app' for production (or 'web:app_with_config()')")
    parser.add_argument("--setup", action="store_true", help="Create the database")
    parser.add_argument("--reset", action="store_true", help="Remove and recreate the database")
    args = parser.parse_args()

    database_exists = os.path.isfile(DB_FILE)

    if args.reset and database_exists: 
        os.remove(DB_FILE)
        database_exists = False
        print("Database file removed")

    if not database_exists:
        with app.app_context():
            db.create_all()
            db.session.commit()
        print("Database tables created")

    if not args.setup and not args.reset:
        app.run(debug=True)
