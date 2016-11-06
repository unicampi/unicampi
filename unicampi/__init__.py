"""UnicamPI"""

import importlib
import inspect
import logging

from cornice import resource
from pyramid.config import Configurator
from pyramid.events import NewRequest

logger = logging.getLogger('unicampi')


class UnicamPI:
    """UnicamPI Envorionment.

    Wraps API and WSGI app.

    Properties
    ----------
    API_VERSION : str, the current version of the API.
    app         : Router, the cornice application already configured.
    config      : Configurator, the application configuration
                  as defined during construction.
    resources   : list, container for all resources collected from views.

    Examples
    --------
    >>> from wsgiref.simple_server import make_server
    >>> from unicampi import UnicamPI
    >>>
    >>> server = make_server('0.0.0.0', 8080, UnicamPI.initiate().app)
    >>> server.serve_forever()

    """

    API_VERSION = '0.0.6'
    app = None
    config = None
    resources = None

    @classmethod
    def initiate(cls, **settings):
        """Initiate UnicamPI, if it's not already.

        :param settings:
            **dict, the settings transmitted to `Configurator` instance.

        :return: cls
        """
        if cls.app is None:
            cls.config = Configurator(settings=settings)
            cls.config.include("cornice")
            # config.include("pyramid_swagger")

            cls._register_resources()

            def add_cors_headers_response_callback(event):
                def cors_headers(request, response):
                    response.headers.update({
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods':
                            'POST,GET,DELETE,PUT,OPTIONS',
                        'Access-Control-Allow-Headers':
                            'Origin, Content-Type, Accept, Authorization',
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Max-Age': '1728000',
                    })

                event.request.add_response_callback(cors_headers)

            cls.config.add_subscriber(add_cors_headers_response_callback,
                                      NewRequest)

            cls.app = cls.config.make_wsgi_app()
        return cls

    @classmethod
    def _register_resources(cls):
        """Auto-load all resources in views module and register them as
        cornice resources.

        :return: cls
        """
        views = importlib.import_module('unicampi.views')

        UnicamPI.resources = []
        resources = inspect.getmembers(
            views, lambda c: (inspect.isclass(c) and
                              issubclass(c, views.BaseResource)))

        for resource_name, resource_cls in resources:
            if resource_cls in (views.BaseResource, views.ModelResource):
                # These are base classes and shouldn't be loaded.
                continue

            # Initialize resource, inferring name and endpoint if necessary.
            resource_cls.initialize()
            # Keep track of what we are loading.
            UnicamPI.resources.append(resource_cls)

            # Signal cornice of the existence eof this resource.
            resource.add_view(resource_cls.get, renderer='json')

            if issubclass(resource_cls, views.ModelResource):
                paths = {'path': resource_cls.endpoint,
                         'collection_path': resource_cls.collection_endpoint}
            else:
                paths = {'path': resource_cls.endpoint}

            cornice_resource = resource.add_resource(resource_cls, **paths)
            cls.config.add_cornice_resource(cornice_resource)

            logger.info('resource %s loaded, endpoints: %s',
                        resource_name, paths)
        return cls
