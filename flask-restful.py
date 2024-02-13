#!flask/bin/python
"""Using Flask-RESTful 

a Flask extension that simplifies the creation of APIs
"""
from flask import Flask, abort, jsonify, url_for, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'king':
        return 'good'
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401, prevent browser from displaying default dialog
    return make_response(jsonify({ 'message': 'Unauthorized access' }), 403)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


class UserAPI(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
                                   help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = '', location = 'json')
        super(TaskListAPI, self).__init__()
    
    def get(self):
        return {'task': [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1 if len(tasks) > 0 else 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str,location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = list(filter(lambda task: task['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        return {'task':marshal(task[0], task_fields)}

    def put(self, id):
        task = list(filter(lambda task: task['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                task[k] = v
        return { 'task': marshal(task, task_fields) }

    def delete(self, id):
        task = list(filter(lambda task: task['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}


api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')
api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint = 'task')


if __name__ == "__main__":
    app.run(debug=True)
