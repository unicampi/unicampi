from .serializers import Serializer


class BaseResource(object):
    """Base Resource.

    Base mixin for any cornice resource.

    """

    name = None
    description = None

    endpoint = None
    collection_endpoint = None
    route_parameters = None

    def __init__(self, request):
        self.request = request
        self.params = Serializer(request.matchdict,
                                 self.route_parameters)

    @classmethod
    def describe(cls, request=None):
        """Describe the resource, such as name, route and parameters.

        :param request: the current request
        :return: dict, a description of the resource.
        """

        description = {
            'name': cls.name,
            'description': cls.description,
            'route': cls.endpoint,
            '_href': request.application_url + cls.endpoint,
        }

        if cls.route_parameters:
            description['parameters'] = params = dict()

            # Some of the processes might be callable, which
            # aren't json serializable. Let's fix that by
            # converting everything to strings first.
            for field, field_desc in cls.route_parameters.items():
                params[field] = {
                    'type': (field_desc['type']
                             if 'type' in field_desc
                             else 'str'),
                }

                if 'examples' in field_desc:
                    params[field]['examples'] = field_desc['examples']

                if 'preprocess' in field_desc:
                    p = field_desc['preprocess']
                    was_list_originally = isinstance(p, (list, tuple, set))
                    p = p if was_list_originally else [p]
                    p = [('?' if callable(e) else e) for e in p]
                    p = p if was_list_originally else p[0]
                    params[field]['preprocess'] = p

        return description

    def options(self):
        return self.describe(request=self.request)

    @classmethod
    def initialize(cls):
        """Initialize resource, inferring whichever information was not
        provided (e.g. verbose name, endpoint).

        :return: cls
        """
        cls.name = cls.name or cls.__name__
        cls.endpoint = cls.endpoint or '/' + cls.name.lower()

        return cls


class ModelResource(BaseResource):
    """Model Resource.

    Base class for model resources (i.e., resources that are associated with
    a repository -- a collection of entries).

    """

    repository = None

    @classmethod
    def initialize(cls):
        """Initialize resource, inferring whichever information was not
        provided (e.g. verbose name, endpoint).

        :return: cls
        """
        cls.name = cls.name or cls.__name__
        cls.collection_endpoint = (cls.collection_endpoint or
                                   '/' + cls.name.lower())
        cls.endpoint = (cls.endpoint or (cls.collection_endpoint + '/{id}'))
        return cls

    def collection_get(self):
        return self.repository().all()

    def get(self):
        try:
            return self.repository().find(self.params['id'])

        except KeyError:
            self.request.errors.add('body', 'id', 'The entry does not exist')
            self.request.errors.status = '404'

    def collection_options(self):
        return self.describe(request=self.request)
