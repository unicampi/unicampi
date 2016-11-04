"""Repositories Base"""


class Repository(object):
    """Repository.

    Base contract for repository classes.

    """

    def __init__(self, **query):
        self.query = query

    def all(self):
        raise NotImplementedError

    def find(self, id):
        raise NotImplementedError

    def where(self, **query):
        """Filter a repository and return all entries that match the filter.

        :param query: dict, parameters that will be used to filter the
                         entries of the repository.
        :return: list, collection of entries.
        """
        return self.filter(**query).all()

    def filter(self, **query):
        """Filter repository entries, resulting in a new repository with a
        different query set.

        :param query: dict, parameters that will be used to filter the
                      entries of the repository.
        :return: Repository-like
        """
        # Transfer old query parameters to new instance.
        new_query = self.query.copy()
        # New parameters override previous ones.
        new_query.update(query)
        # Instantiate a new repository, of this class, with the new query.
        return self.__class__(**new_query)
