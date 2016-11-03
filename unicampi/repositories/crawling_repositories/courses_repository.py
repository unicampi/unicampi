# -- coding: utf-8 --

"""Courses Repository"""

# Author: Lucas David -- <ld492@drexel.edu>
# License: GPL 3.0

import requests
from bs4 import BeautifulSoup

from . import urls, utils
from ..base import Repository


class CoursesRepository(Repository):
    def all(self):
        institute = self.matching.get('institute')

        if institute is None:
            raise NotImplementedError(
                'Courses repository does not support global fetching just '
                'yet. Please specify an institute_id using the '
                '"CoursesRepository.filter" method.')

        page = requests.get(urls.COURSES_URL % institute)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        data = tds[1].find_all('td')
        # strip and remove raw content
        data = [el.text.strip() for el in data[1:]]

        courses = []
        for sub in data:
            code = sub[:5]
            name = sub[5:]

            courses.append({
                'nome': name.strip(),
                'sigla': code.replace(' ', '_'),
            })

        return courses

    def find(self, id):
        try:
            page = requests.get(urls.COURSES_URL % id)
            soup = BeautifulSoup(page.text, 'lxml')
            tds = soup.find_all('table')

            data = tds[1].find_all('td')[1]

            f = utils.ContentFinder(data.text)

            main_info = f.split[0]
            code = main_info[:5]
            name = main_info[5:].strip()

            content = f.find_by_content('Ementa:', offset=1)
            credits = f.find_by_content('Créditos:', offset=0)[-3:]
            requires_list = f.find_by_content('Pré-Requisitos:',
                                              offset=1,
                                              end_pattern='Turma:')

            req_dates = requires_list[::2]
            req_values = requires_list[1::2]

            # split 'or' requirements
            req_values = [v.strip().split(' / ') for v in req_values]

            # split 'and' requirements
            for i in range(len(req_values)):
                req_values[i] = [v.strip().split('  ') for v in req_values[i]]

            requires = dict(zip(req_dates, req_values))

            return {
                'nome': name,
                'sigla': code.replace(' ', '_'),
                'ementa': content,
                'pré-requisitos': requires,
                'créditos': int(credits),
            }

        except (IndexError, KeyError, UnboundLocalError):
            raise KeyError('unknown entry %s' % id)
