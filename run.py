"""Run"""

from wsgiref.simple_server import make_server

from pyramid.config import Configurator

from unicampi import main

SERVER = '0.0.0.0'
PORT = 8080


def runserver():
    try:
        print('server starting at %s:%i' % (SERVER, PORT))

        config = Configurator()
        app = main(config)
        server = make_server(SERVER, PORT, app)
        server.serve_forever()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    runserver()
