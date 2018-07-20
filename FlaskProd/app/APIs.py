from flask import Blueprint
from flask_restplus import Api, Resource, fields, reqparse


KingBase = Blueprint('KingBase', __name__)
api = Api(KingBase, version='1.0', title='TodoMVC API', doc='/swagger-ui.html', description='A simple TodoMVC API',
          contact_email='lwc@quuedu.com', contact='Alex')

base_path = '/bigData/api/v1'

KingKpi = api.namespace('KingKpi', description='刷题王考核', path=base_path)
ns1 = api.namespace('ns1', description='TODO1 operations1', path=base_path)

availability = api.model('Availability', {
    'monday': fields.String(required=True, description='Availability of the therapist on Monday'),
    'task1': fields.String(required=True, description='The task1 details')
})

todo = api.model('Todo', {
    'schoolId': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'availability': fields.Nested(availability, as_list=True)

})


def get_trace_id():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


class GetInfo(object):
    def __init__(self):
        self.school_id='schoolId'

    # def get(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("foo", type = str, required = True,
    #     location = ('values', 'json', 'form','data'),
    #     help = "Missing 'foo' argument")
    #     args=parser.parse_args()
    #     foo=args['foo']
    # return __find_foo(foo)


test_ava = [
    {"name": "Id", "description": "Id", "required": True, "type": "integer"},
    {"name": "schoolId", "description": "schoolId", "required": True, "type": "integer"},
]


@KingKpi.route('/getKpi')
class TodoList(Resource):
    test_a2 = api.model('Availability', {
        'monday': fields.String(required=True, description='Availability of the therapist on Monday'),
        'task1': fields.String(required=True, description='The task1 details')
    })
    test_a1 = api.parser()
    test_a1.add_argument('schoolId', required=True, type=int, help='school_id', location='query')
    test_a1.add_argument('startTime', type=int, help='start_time', location='query')
    test_a1.add_argument('endTime', type=int, help='end_time', location='query')


    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @KingKpi.doc('list_todos', security=None)
    #@KingKpi.expect(test_a1)
    @KingKpi.expect(test_a2)
    # @KingKpi.marshal_list_with(todo)
    @KingKpi.marshal_with(todo, code=200)
    def get(self):
        '''List all tasks'''
        parser = reqparse.RequestParser()
        parser.add_argument('schoolId', type=int)
        parser.add_argument('startTime', type=int)
        parser.add_argument('endTime', type=int)
        args = parser.parse_args()
        #data = test_a1.values.get('password')
        print(args['schoolId'])

        return args, 200

    # @KingKpi.doc('create_todo')
    # @KingKpi.expect(todo)
    # @KingKpi.marshal_with(todo, code=201)
    # def post(self):
    #     '''Create a new task'''
    #     return DAO.create(api.payload), 201


@KingKpi.route('/<int:id>')
@KingKpi.response(404, 'Todo not found')
@KingKpi.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @KingKpi.doc('get_todo')
    @KingKpi.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    # @KingKpi.doc('delete_todo')
    # @KingKpi.response(204, 'Todo deleted')
    # def delete(self, id):
    #     '''Delete a task given its identifier'''
    #     DAO.delete(id)
    #     return '', 204
    #
    # @KingKpi.expect(todo)
    # @KingKpi.marshal_with(todo)
    # def put(self, id):
    #     '''Update a task given its identifier'''
    #     return DAO.update(id, api.payload)

@ns1.route('/test/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @ns1.doc('list_todos')
    @ns1.marshal_list_with(todo)
    @ns1.marshal_with(todo, code=400)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns1.doc('create_todo')
    @ns1.expect(todo)
    @ns1.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201
