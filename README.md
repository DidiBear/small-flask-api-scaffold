# Small-Flask-API-scaffold

This repo is a scaffold of a small flask API app.

Web app feature are added into `web.py`
Database object are added into `model.py`


# Deploy

## Setup and Launch

Install dependencies :

    $ pip install --user -r requirement.txt

Create database :

    $ python web.py --setup

Launch the app with the WSGI :

    $ gunicorn --workers 4 --bind 0.0.0.0:8080 web:app

## Debug 

Launch the app in debug mode :

    $ python web.py

Reset database :

    $ python web.py --reset

Launch tests : 

    $ pytest test.py


## Specific config when stating the application

Normally, the app is started with :

    $ gunicorn web:app

Additionnaly, you can change app config by launching the app with 

    $ gunicorn 'web:app_with_config(...)'


# Administration 

## GUI

Go to `/admin` to manage the database with the GUI

## API

Go to `/api/<model>` to use the generated REST api ([Documentation][1])

[Querying through the api][2]

[1]:https://flask-restless.readthedocs.io/en/stable/customizing.html
[2]:https://flask-restless.readthedocs.io/en/stable/searchformat.html#examples

## Web Framework : Flask

Extensions :
* `Flask` : Manage HTTP requests
* `Flask-SQLAlchemy` : manage SQL database
* `Flask-Admin` : GUI for managing database
* `Flask-Restless` : API REST upon database objects
* `Flask-Testing` : for testing
