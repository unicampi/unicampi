
class OnlineFilter(object):
    """Online Filter.

    Provides a filtering interface for entries, allowing the user to perform
    more complex queries such as `...Repository.filter(id__not_in=[1, 2])`.

    Example
    -------
    >>> users = [{'name': n} for n in ('lucas', 'kelly', 'adam', 'jessica')]
    >>> OnlineFilter(name__in=['lucas', 'jessica']).commit(users)
    >>> [{'name': 'lucas'}, {'name': 'jessica'}]

    """

    VALID_OPERATORS = {
        'equals': lambda entry, field, value: entry.get(field) == value,
        'not_equals': lambda entry, field, value: entry.get(field) != value,
        'in': lambda entry, field, value: entry.get(field) in value,
        'not_in': lambda entry, field, value: entry.get(field) not in value,
        'contains': lambda entry, field, value: value in entry.get(field),
        'not_contains': (lambda entry, field, value:
                         value not in entry.get(field)),
    }

    def __init__(self, **query):
        self.query = query
        self.entries = None

    def commit(self, entries):
        matched_entries = []

        for entry in entries:
            matches = True

            for field_and_maybe_operator, value in self.query.items():
                parts = field_and_maybe_operator.split('__')

                if len(parts) == 1:
                    # No operator specified, assume equals.
                    field = '__'.join(parts)
                    operator = 'equals'
                else:
                    field = '__'.join(parts[:-1])
                    operator = parts[-1]

                if operator not in self.VALID_OPERATORS:
                    raise RuntimeError('unknown operator {%s}' % operator)

                matches = self.VALID_OPERATORS[operator](entry, field, value)
                if not matches:
                    break

            if matches:
                matched_entries.append(entry)
        return matched_entries


class ContentFinder(object):
    def __init__(self, data, separator='\n'):
        self.data = data
        self.split = [s.strip() for s in data.split(separator) if s.strip()]

    def find_by_content(self, pattern, pos=0, offset=0,
                        count=None, end_pattern=None):

        # decode if Python 2.x
        if hasattr(pattern, 'decode'):
            pattern = pattern.decode('utf-8')  # no cover

        for piece, i in zip(self.split, range(len(self.split))):
            if pattern in piece:
                if pos:
                    pos -= 1
                else:
                    start_at = i
                    break

        if count:
            return self.split[start_at + offset:start_at + count + offset]

        if end_pattern:  # no cover
            for piece, i in zip(self.split[start_at:],
                                range(start_at, len(self.split))):
                if end_pattern in piece:
                    end_idx = i
                    break

            return self.split[start_at + offset:end_idx]

        else:
            return self.split[start_at + offset]
