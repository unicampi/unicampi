"""Institutes Repository"""

# Author: Lucas David -- <ld492@drexel.edu>
# License: GPL 3.0

import requests
from bs4 import BeautifulSoup

from unicampi.repositories.crawling_repositories import urls
from ..base import Repository


class InstitutesRepository(Repository):
    def all(self):
        if self.matching:
            raise NotImplementedError('institutes repository does not '
                                      'support filtering just yet. You can '
                                      'either retrieve "all" institutes or '
                                      '"find" one.')

        page = requests.get(urls.INSTITUTES_URL)
        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        # Get 3rd table.
        data = tds[3].find_all('td')
        data = [el.text.strip() for el in data]

        codes = data[::2]
        names = data[1::2]

        return [{'sigla': c, 'nome': n} for c, n in zip(codes, names)]

    def find(self, id):
        id = str(id).upper()

        for institute in self.all():
            if institute['sigla'].upper() == id:
                return institute

        raise KeyError('unknown entry %s' % id)

    def query(self, **matching):
        raise NotImplementedError
