"""Main entry point
"""
from pyramid.config import Configurator

API_VERSION = '0.04'

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    #config.include("pyramid_swagger")
    config.scan("unicampi.views")
    return config.make_wsgi_app()

