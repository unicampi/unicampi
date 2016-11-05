# coding:utf-8

"""Views"""

from . import UnicamPI
from .core.views import BaseResource, ModelResource
from .repositories import (CoursesRepository, EnrollmentsRepository,
                           InstitutesRepository, OfferingsRepository)


class Docs(BaseResource):
    name = 'Documentação'
    description = 'Mapa da UnicamPI.'
    endpoint = '/'

    def get(self):
        return {
            'api_version': UnicamPI.API_VERSION,
            'map': [r.describe(request=self.request) for r in
                    UnicamPI.resources]
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

    repository = InstitutesRepository


class Courses(ModelResource):
    name = 'Disciplinas'
    description = 'Disciplinas de um determinado instituto na UNICAMP.'

    endpoint = '/disciplinas/{id}'
    collection_endpoint = '/institutos/{instituto}/disciplinas'

    route_parameters = {
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
        courses = CoursesRepository()

        if 'instituto' in self.params:
            courses = courses.filter(institute=self.params['instituto'])

        return courses


class Offerings(ModelResource):
    name = 'Oferecimentos'
    description = 'Turmas de uma determinada disciplina e período.'
    collection_endpoint = ('/periodos/{periodo}'
                           '/oferecimentos/{disciplina}/turmas')

    route_parameters = {
        'periodo': {
            'preprocess': ['lowercase', lambda x: x.lower().split('s')],
            'examples': ['2015s1', '2014s2'],
        },
        'disciplina': {
            'preprocess': 'uppercase',
            'examples': ['MC102', 'mc878'],
        },
    }

    def repository(self):
        year, term = self.params['periodo']

        return (OfferingsRepository()
                .filter(year=year, term=term,
                        course=self.params['disciplina']))


class Enrollments(ModelResource):
    name = 'Matrículas'
    description = 'Matrículas em uma turma.'

    collection_endpoint = ('/periodos/{periodo}/oferecimentos/{disciplina}'
                           '/turmas/{turma}/matriculados')

    route_parameters = {
        'periodo': {
            'preprocess': ['lowercase', lambda x: x.lower().split('s')],
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
                        offering=self.params['turma']))
