# coding:utf-8

"""Offerings Repository"""

# Author: Lucas David -- <ld492@drexel.edu>
# License: GPL 3.0

import requests
from bs4 import BeautifulSoup

from . import urls, utils
from ..base import Repository


class OfferingsRepository(Repository):
    def all(self):
        self._assert_valid_query()

        with requests.Session() as s:
            token_page = s.get(urls.PUBLIC_MENU_URL)
            token = token_page.content[1839:1871].decode('ascii')

            page = s.get(urls.OFFERINGS_URL % (token,
                                               self.matching['term'],
                                               self.matching['year'],
                                               self.matching['course'],
                                               'a'))
        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        # Get table 8
        data = tds[8]
        data = [lin.find_all('td') for lin in data.find_all('tr')[2:]]

        return [{
                    'turma': offering[0].text,
                    'vagas': offering[1].text,
                    'matriculados': offering[2].text,
                } for offering in data]

    def find(self, id):
        self._assert_valid_query()

        with requests.Session() as s:
            token_page = s.get(urls.PUBLIC_MENU_URL)
            token = token_page.content[1839:1871].decode('ascii')

            page = s.get(urls.OFFERING_URL % (token,
                                              self.matching['term'],
                                              self.matching['year'],
                                              self.matching['course'],
                                              id))
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            tds = soup.find_all('table')

            # Get table 6 (general info)
            data = tds[6]

            f = utils.ContentFinder(data.text)
            teacher = f.find_by_content('Docente:').split(':', 1)[1].strip()
            situation = f.find_by_content('Situação:').split(':', 1)[1].strip()

            # Data is type "Situação:  25 vagas  -  12 matriculados" 
            vacancy, registered = situation.split('-')

            vacancies = vacancy.strip().split(' ', 1)[0]
            registered = registered.strip().split(' ', 1)[0]

            # Get table 8 (students)
            students_data = tds[8].find_all('td')

            # Remove heder
            students_data = [s.text for s in students_data[7:]]

            students = []
            for i in range(0, len(students_data), 6):
                students.append({
                    'ra': students_data[i + 1],
                    'nome': students_data[i + 2].strip(),
                    'curso': students_data[i + 3],
                    'tipo': students_data[i + 4],
                    'modalidade': students_data[i + 5],
                })

            offering = {
                'turma': id,
                'sigla': self.matching['course'],
                'ano': self.matching['year'],
                'semestre': self.matching['term'],
                'professor': teacher,
                'vagas': vacancies,
                'matriculados': registered,
                'alunos': students
            }

            return offering

        except (UnboundLocalError, IndexError, KeyError):
            raise KeyError('unknown entry %s' % id)

    def _assert_valid_query(self):
        if not {'term', 'year', 'course'}.issubset(self.matching.keys()):
            raise RuntimeError('Offerings must be filtered by term, year and '
                               'course. Only then they be fetched.')
