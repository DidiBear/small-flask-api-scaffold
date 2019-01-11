# launch test with : $ pytest test.py

import unittest
import os
from flask import Flask
from flask_testing import TestCase
from model import db, Task
from web import app

DB_FILE = "./test.db"

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_FILE
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(DB_FILE)
        except OSError:
            pass


class TestHello(TestApp):
    
    def test_hello_ok(self):
        response = self.client.get("/hello/Jean")
        self.assert200(response)
        
        assert response.json["status"] == "success"
        assert response.json["data"] == "Hello Jean !"

    def test_hello_ko(self):
        response = self.client.get("/hello")
        self.assert400(response)
        
        assert response.json["status"] == "error"
        assert response.json["message"]


class TestSimpleTest(unittest.TestCase):

    def test_addition(self):
        assert 18*2 == 36
        
class TestSearchTasks(TestApp):

    def setUp(self):
        super(TestSearchTasks, self).setUp()

        task1 = Task(task="my task 1")
        task2 = Task(task="my task 2")
        
        db.session.add_all((task1, task2))
        db.session.commit()

    def test_search_several_task(self):
        response = self.client.get("/search_tasks/task")
        self.assert200(response)
        
        assert response.json["status"] == "success"
        data = response.json["data"]

        assert len(data) == 2
        assert data[0]["task"] == "my task 1"
        assert data[1]["task"] == "my task 2"
        
    def test_search_one_task(self):
        response = self.client.get("/search_tasks/task 1")
        self.assert200(response)
        
        assert response.json["status"] == "success"
        data = response.json["data"]

        assert len(data) == 1
        assert data[0]["task"] == "my task 1"
        
    def test_search_no_task(self):
        response = self.client.get("/search_tasks/nothing")
        self.assert200(response)
        
        assert response.json["status"] == "success"
        assert len(response.json["data"]) == 0
        

if __name__ == '__main__':
    unittest.main()

