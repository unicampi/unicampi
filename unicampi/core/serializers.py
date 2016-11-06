class Serializer(object):
    """Serializer Base Class.

    Base contract for serializers. These classes are responsible of take as
    input the data of an HTTP request (which always comes as strings) and
    digest it according to a schema.

    Parameters
    ----------
    data  : dict, the data of the request.
    schema : dict, the schema representing the conversion.

    Examples
    --------
    >>> schema = {'id': {'type': int}, 'age': {'type': int}}
    >>> d = {'id': '4', 'name': 'Stan Marshal', 'age': '24'}
    >>> s = Serializer(d, schema)
    >>>
    >>> d['id'], d['name'], d['age']
    ... '4', 'Stan Marshal', '24'
    >>>
    >>> s['id'], s['name'], s['age']
    ... 4, 'Stan Marshal', 24

    """

    _preprocesses = {
        'uppercase': lambda x: x.upper(),
        'lowercase': lambda x: x.lower(),
        'split-year-term': lambda x: x.lower().rstrip().split('s'),
    }

    def __init__(self, data, schema):
        self.data = data.copy()
        self.schema = schema

        if schema:
            for field, description in self.schema.items():
                if field not in self.data:
                    continue

                if 'type' in description:
                    self.data[field] = description['type'](self.data[field])

                if 'preprocess' in description:
                    preprocess = description['preprocess']

                    if not isinstance(preprocess, (list, tuple, set)):
                        # preprocess can be a single operation or a list
                        # of operations: normalize it.
                        preprocess = [preprocess]

                    for p in preprocess:
                        if isinstance(p, str):
                            # If it's a string, refer to
                            # our map of pre-processes.
                            if p not in self._preprocesses:
                                raise KeyError('unknown preprocess %s for %s'
                                               ' field' % (p, field))

                            p = self._preprocesses[p]

                        self.data[field] = p(self.data[field])

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return item in self.data
