# coding: utf-8

"""Crawling Repositories

These test_repositories crawl the web after their data.

"""

import requests
from bs4 import BeautifulSoup

from . import urls, base

__all__ = ['CoursesRepository', 'EnrollmentsRepository',
           'InstitutesRepository', 'OfferingsRepository']


class InstitutesRepository(base.CrawlerRepository):
    def _fetch_and_parse_all(self):
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
        try:
            return self.where(sigla=id)[0]
        except IndexError:
            raise KeyError('unknown entry %s' % id)


class CoursesRepository(base.CrawlerRepository):
    _required_querying_fields = {'institute'}

    def _fetch_and_parse_all(self):
        page = requests.get(urls.COURSES_URL % self.query['institute'])
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

    def _fetch_and_parse_one(self, id):
        page = requests.get(urls.COURSES_URL % id)
        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        data = tds[1].find_all('td')[1]

        f = base.ContentFinder(data.text)

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
            'requisitos': requires,
            'créditos': int(credits),
        }


class OfferingsRepository(base.CrawlerRepository):
    _required_querying_fields = {'term', 'year', 'course'}

    def _fetch_and_parse_all(self):
        with requests.Session() as s:
            token_page = s.get(urls.PUBLIC_MENU_URL)
            token = token_page.content[1839:1871].decode('ascii')

            page = s.get(urls.OFFERINGS_URL % (token,
                                               self.query['term'],
                                               self.query['year'],
                                               self.query['course'],
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

    def _fetch_and_parse_one(self, id):
        with requests.Session() as s:
            token_page = s.get(urls.PUBLIC_MENU_URL)
            token = token_page.content[1839:1871].decode('ascii')

            page = s.get(urls.OFFERING_URL % (token,
                                              self.query['term'],
                                              self.query['year'],
                                              self.query['course'],
                                              id))
        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')

        # Get table 6 (general info)
        data = tds[6]

        f = base.ContentFinder(data.text)
        teacher = f.find_by_content('Docente:').split(':', 1)[1].strip()
        situation = f.find_by_content('Situação:').split(':', 1)[1].strip()

        # Data is type "Situação:  25 vagas  -  12 matriculados" 
        vacancy, registered = situation.split('-')

        vacancies = vacancy.strip().split(' ', 1)[0]
        registered = registered.strip().split(' ', 1)[0]

        # Get table 8 (students)
        students_data = tds[8].find_all('td')

        # Remove header
        students_data = [_s.text for _s in students_data[7:]]

        students = []
        for i in range(0, len(students_data), 6):
            students.append({
                'ra': students_data[i + 1],
                'nome': students_data[i + 2].strip(),
                'curso': students_data[i + 3],
                'tipo': students_data[i + 4],
                'modalidade': students_data[i + 5],
            })

        return {
            'turma': id,
            'sigla': self.query['course'],
            'ano': self.query['year'],
            'semestre': self.query['term'],
            'professor': teacher,
            'vagas': vacancies,
            'matriculados': registered,
            'alunos': students
        }


class EnrollmentsRepository(OfferingsRepository):
    """Enrollments CrawlerRepository.

    Enrollments are always associated to a class (the offering of a course).
    Because OfferingsRepository already parses and provides us with the
    enrollments when searching for a given class, we need only to sub-class
    it and filter for said enrollments.

    """

    _required_querying_fields = {'term', 'year', 'course', 'offering'}

    def all(self):
        self._assert_valid_query()
        enrollments = (super(EnrollmentsRepository, self)
                       .find(id=self.query['offering'])['alunos'])

        new_query = {k: v for k, v in self.query.items() if
                     k not in self._required_querying_fields}
        return base.OnlineFilter(**new_query).commit(enrollments)

    def find(self, id):
        try:
            return self.where(ra=id)[0]
        except IndexError:
            raise KeyError('unknown entry %s' % id)
