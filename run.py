from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from unicampi import main

SERVER = '0.0.0.0'
PORT = 8080

config = Configurator()
app = main(config)
server = make_server(SERVER, PORT, app)
server.serve_forever()
