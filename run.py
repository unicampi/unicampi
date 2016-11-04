from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from unicampi import main
from pyramid.events import NewRequest

SERVER = '0.0.0.0'
PORT = 8080

config = Configurator()
def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)
config.add_subscriber(add_cors_headers_response_callback, NewRequest)
app = main(config)
server = make_server(SERVER, PORT, app)
server.serve_forever()
