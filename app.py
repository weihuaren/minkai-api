from flask import Flask
from flask_restful import Api, Resource
from resources.tickets import Ticket, TicketList
app = Flask(__name__)
api = Api(app)

api.add_resource(Ticket, '/tickets/<int:ticket_id>')
api.add_resource(TicketList, '/tickets')

if __name__ == '__main__':
    app.run(debug=True)