from ..base import Repository
from .utils import OnlineFilter


class CrawlerRepository(Repository):
    """Crawler Repository.

    Base repository class for test_crawlers.

    """

    _required_querying_fields = set()

    def _assert_valid_query(self):
        if not self._required_querying_fields.issubset(self.query.keys()):
            raise RuntimeError('Offerings must be filtered by %s. '
                               'Only then they be fetched.'
                               % self._required_querying_fields)

    def all(self):
        self._assert_valid_query()
        entries = self._fetch_and_parse_all()
        new_query = {k: v for k, v in self.query.items() if
                     k not in self._required_querying_fields}
        return OnlineFilter(**new_query).commit(entries)

    def find(self, id):
        try:
            return self._fetch_and_parse_one(id)
        except (IndexError, KeyError, UnboundLocalError):
            raise KeyError('unknown entry %s' % id)

    def _fetch_and_parse_all(self):
        raise NotImplementedError

    def _fetch_and_parse_one(self, id):
        raise NotImplementedError
