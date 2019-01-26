from flask_restful import Resource, reqparse, abort, fields, marshal_with

FIELDS_CONFIG = { 
    'summary' : {
        'required' : True,
        'type' : str,
    },
    'description' : {
        'required' : False,
        'type' : str,
    },
}

WORKFLOW_CONFIG = {
    'default' : 'open',
    'statuses' : ['open', 'in progress','done'],
}

parser = reqparse.RequestParser()

list(map(lambda x: parser.add_argument(
        x, 
        dest=x,
        type=FIELDS_CONFIG.get(x).get('type'),
        location='form', 
        required=FIELDS_CONFIG.get(x).get('required'),
        help='The ticket\'s ' + x,
        ), 
        FIELDS_CONFIG.keys()
        )
)   

parser.add_argument(
    'status', 
    dest='status',
    type=str, location='form',
    default=WORKFLOW_CONFIG.get('default'), 
    choices=WORKFLOW_CONFIG.get('default'), 
    help='The ticket\'s status',
)

ticket_fields = {
    'summary': fields.String,
    'description': fields.String,
    'status': fields.String,
    'temp' : fields.Integer
}

ticket_list = {
    1 : {
            'summary': 'welcome',
            'description': 'get started',
            'status': 'open',
        },
}

def abort_if_ticket_doesnt_exist(ticket_id):
    if ticket_id not in ticket_list:
        abort(404, message="Ticket {} doesn't exist".format(ticket_id))
        
class Ticket(Resource):
    @marshal_with(ticket_fields)
    def get(self, ticket_id):
        args = parser.parse_args()
        abort_if_ticket_doesnt_exist(ticket_id)
        return ticket_list[ticket_id]

    def delete(self, ticket_id):
        abort_if_ticket_doesnt_exist(ticket_id)
        del ticket_list[ticket_id]
        return '', 204
        
    @marshal_with(ticket_fields)
    def put(self, ticket_id):
        args = parser.parse_args()
        ticket = {
            'summary': args['summary'],
            'description': args['description'],
            'status': args['status'],
        }
        ticket_list[ticket_id] = ticket
        return task, 201

class TicketList(Resource):
    def get(self):
        return ticket_list
    
    @marshal_with(ticket_fields)
    def post(self):
        args = parser.parse_args()
        print(args['summary'])
        ticket_id = max(ticket_list.keys()) + 1
        ticket_list[ticket_id] = {
            'summary': args['summary'],
            'description': args['description'],
            'status': args['status'],
        }
        return ticket_list[ticket_id], 201

