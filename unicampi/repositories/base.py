"""Repositories Base"""

# Author: Lucas David -- <ld492@drexel.edu>
# License: GPL 3.0


class Repository(object):
    """Repository.

    Base contract for repository classes.

    """

    def __init__(self, **matching):
        self.matching = matching

    def all(self):
        raise NotImplementedError

    def find(self, id):
        raise NotImplementedError

    def query(self, **matching):
        """Filter a repository and return all entries that match the filter.

        :param matching: dict, parameters that will be used to filter the
                         entries of the repository.
        :return: list, collection of entries.
        """
        return self.filter(**matching).all()

    def filter(self, **matching):
        """Filter repository entries, resulting in a new repository with a
        different matching set.

        :param matching: dict, parameters that will be used to filter the
                         entries of the repository.
        :return: Repository-like
        """
        # Transfer old matching parameters to new instance.
        _m = self.matching.copy()
        # New parameters override previous ones.
        _m.update(matching)
        # Instantiate a new repository, of this class, with the new matching.
        return self.__class__(**_m)
