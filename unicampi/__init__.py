"""Main entry point
"""
from pyramid.config import Configurator
from pyramid.events import NewRequest
API_VERSION = '0.04'

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    #config.include("pyramid_swagger")
    config.scan("unicampi.views")

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
    return config.make_wsgi_app()
