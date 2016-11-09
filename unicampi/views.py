# coding:utf-8

"""Views"""

from . import UnicamPI
from .core.views import BaseResource, ModelResource
from .repositories import (InstitutesRepository,
                           ActiveCoursesRepository, ActiveInstitutesRepository,
                           LecturesRepository, EnrollmentsRepository)


class Docs(BaseResource):
    name = 'Documentação'
    description = 'Mapa da UnicamPI.'
    endpoint = '/'

    def get(self):
        return {
            'api_version': UnicamPI.API_VERSION,
            'map': sorted([r.describe(request=self.request) for r in
                           UnicamPI.resources], key=lambda d: d['route'])
        }


class Institutes(ModelResource):
    name = 'Institutos'
    description = 'Recupera institutos da UNICAMP.'
    collection_endpoint = '/institutos'

    route_parameters = {
        'id': {
            'preprocess': 'uppercase',
            'examples': ['IC', 'feec', 'iFcH'],
        },
    }

    def repository(self):
        institutes = InstitutesRepository()

        return institutes


class ActiveInstitutes(ModelResource):
    name = 'Institutos ativos'
    description = ('Recupera institutos da UNICAMP que oferecem disciplinas',
                   ' em um periodo')
    endpoint = '/institutos/{id}/periodos/{periodo}'
    collection_endpoint = '/institutos/periodos/{periodo}'

    route_parameters = {
        'periodo': {
            'preprocess': 'split-year-term',
            'examples': ['2015s1', '2014s2'],
        },
        'id': {
            'preprocess': 'uppercase',
            'examples': ['IC', 'feec', 'iFcH'],
        },
    }

    def repository(self):
        year, term = self.params['periodo']
        institutes = ActiveInstitutesRepository(term=term)

        return institutes


class ActiveCourses(ModelResource):
    name = 'Disciplinas ativas'
    description = ('Disciplinas ativas em um periodo em'
                   'determinado instituto na UNICAMP.')

    endpoint = '/disciplinas/{id}/periodos/{periodo}'
    collection_endpoint = '/institutos/{instituto}/periodos/{periodo}/disciplinas'

    route_parameters = {
        'periodo': {
            'preprocess': 'split-year-term',
            'examples': ['2015s1', '2014s2'],
        },
        'id': {
            'preprocess': 'uppercase',
            'examples': ['MC102', 'mc878'],
        },
        'instituto': {
            'preprocess': 'uppercase',
            'examples': ['IC', 'feec', 'iFcH'],
        },
    }

    def repository(self):
        year, term = self.params['periodo']

        courses = ActiveCoursesRepository().filter(term=term)

        if 'instituto' in self.params:
            courses = courses.filter(institute=self.params['instituto'])

        return courses


class Lectures(ModelResource):
    name = 'Oferecimentos'
    description = 'Turmas de uma determinada disciplina e período.'
    collection_endpoint = ('/disciplinas/{disciplina}'
                           '/periodos/{periodo}/turmas')

    route_parameters = {
        'periodo': {
            'preprocess': 'split-year-term',
            'examples': ['2015s1', '2014s2'],
        },
        'disciplina': {
            'preprocess': 'uppercase',
            'examples': ['MC102', 'mc878'],
        },
    }

    def repository(self):
        year, term = self.params['periodo']

        return (LecturesRepository()
                .filter(year=year, term=term,
                        course=self.params['disciplina']))


class Enrollments(ModelResource):
    name = 'Matrículas'
    description = 'Matrículas em uma turma.'

    collection_endpoint = ('/disciplinas/{disciplina}'
                           '/periodos/{periodo}'
                           '/turmas/{turma}/matriculados')

    route_parameters = {
        'periodo': {
            'preprocess': 'split-year-term',
            'examples': ['2015s1', '2014s2'],
        },
        'disciplina': {
            'preprocess': 'uppercase',
            'examples': ['MC102', 'mc878'],
        },
        'turma': {
            'preprocess': 'lowercase',
            'examples': ['a', 'B']
        },
    }

    def repository(self):
        year, term = self.params['periodo']

        return (EnrollmentsRepository()
                .filter(year=year, term=term,
                        course=self.params['disciplina'],
                        lecture=self.params['turma']))
