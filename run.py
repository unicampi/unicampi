"""Run"""
import logging
from wsgiref.simple_server import make_server

from unicampi import UnicamPI

SERVER = '0.0.0.0'
PORT = 8080
LOGGING_LEVEL = logging.INFO

logger = logging.getLogger('unicampi')


def runserver():
    logging.basicConfig(level=LOGGING_LEVEL)
    logger.setLevel(LOGGING_LEVEL)

    try:
        UnicamPI.initiate()
        server = make_server(SERVER, PORT, UnicamPI.app)

        logger.info('serving at http://%s:%i' % (SERVER, PORT))
        server.serve_forever()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    runserver()
