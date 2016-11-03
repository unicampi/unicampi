# coding:utf-8

"""Views"""

# Author: gabisurita -- <gabsurita@gmail.com>
# License: GPL 3.0

from cornice.resource import resource

from .repositories import (CoursesRepository, EnrollmentsRepository,
                           InstitutesRepository, OfferingsRepository)

ENDPOINTS = {
    'Institutos': {
        'collection_path': '/institutos',
        'path': '/institutos/{id}',
    },
    'Disciplinas': {
        'collection_path': '/institutos/{instituto}/disciplinas',
        'path': '/disciplinas/{id}',
    },
    'Oferecimentos': {
        'collection_path': '/periodos/{periodo}/oferecimentos/{disciplina}',
        'path': '/periodos/{periodo}/oferecimentos/{disciplina}/turma/{id}',
    },
    'Matriculados': {
        'collection_path': '/periodos/{periodo}/oferecimentos/{disciplina}'
                           '/turma/{turma}/matriculados',
        'path': '/periodos/{periodo}/oferecimentos/{disciplina}/turma/{turma}'
                '/matriculados/{id}',
    },
}


class BaseResource(object):
    """Base Resource.

    Base mixin for any cornice resource.

    """

    def __init__(self, request):
        self.request = request

    @property
    def params(self):
        return self.request.matchdict


class ModelResource(BaseResource):
    """Model Resource.

    Base class for model resources (i.e., resources that are associated with
    a repository -- a collection of entries).

    """

    repository = None

    def collection_get(self):
        return self.repository().all()

    def get(self):
        try:
            return self.repository().find(self.params['id'])

        except KeyError:
            self.request.errors.add('body', 'id', 'The entry does not exist')
            self.request.errors.status = '404'


@resource(path='/')
class Hello(BaseResource):
    def get(self):
        return {'path': ENDPOINTS}


@resource(**ENDPOINTS['Institutos'])
class Institute(ModelResource):
    repository = InstitutesRepository


@resource(**ENDPOINTS['Disciplinas'])
class Courses(ModelResource):
    def repository(self):
        return (CoursesRepository()
                .filter(institute=self.params.get('instituto')))


@resource(**ENDPOINTS['Oferecimentos'])
class Offering(ModelResource):
    def repository(self):
        year, term = self.params['periodo'].lower().split('s', 1)
        course = self.params['disciplina'].upper()

        return (OfferingsRepository()
                .filter(year=year, term=term, course=course))


@resource(**ENDPOINTS['Matriculados'])
class Enrollments(ModelResource):
    def repository(self):
        year, term = self.params['periodo'].lower().split('s', 1)
        course = self.params['disciplina'].upper()
        offering = self.params['turma'].lower()

        return (EnrollmentsRepository()
                .filter(year=year, term=term, course=course,
                        offering=offering))
