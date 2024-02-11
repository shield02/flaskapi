#!flask/bin/python
"""Using Flask-RESTful 

a Flask extension that simplifies the creation of APIs
"""
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api()

class UserAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
                                   help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = '', location = 'json')
        super(TaskListAPI, self).__init__()
    
    def get(self):
        pass

    def post(self):
        pass

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str,location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')
api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint = 'task')
