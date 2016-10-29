from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from __init__ import main

config = Configurator()
app = main(config)
server = make_server('0.0.0.0', 8080, app)
server.serve_forever()
