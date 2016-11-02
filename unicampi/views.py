# coding:utf-8

from cornice.resource import resource, view
from cornice import Service
from unicampi import dacParser

ENDPOINTS = {
    'Institutos': {
        'collection_path':'/{periodo}/institutos',
        'path': '/{periodo}/institutos/{sigla}',
     }, 
    'Disciplinas': {
        'collection_path':'/{periodo}/instituto/{instituto}/disciplinas',
        'path': '/{periodo}/disciplinas/{sigla}',
     },
    'Oferecimentos': {
        'collection_path': '/{periodo}/oferecimentos/{sigla}',
        'path': '/{periodo}/oferecimentos/{sigla}/{turma}',
     },
    'Matriculados': {
        'path': '/{periodo}/oferecimentos/{sigla}/{turma}/matriculados',
     },
}


@resource(path='/')
class Hello(object):
    
    def __init__(self, request):
        self.request = request
    
    def get(self):
        return {'path': ENDPOINTS}


class ApiResource(object):

    def __init__(self, request):
        self.request = request
        self.periodo = request.matchdict['periodo'].lower()
        self.ano, self.sem = self.periodo.split('s', 1)


@resource(**ENDPOINTS['Institutos'])
class Institute(ApiResource):

    def __init__(self, request):
        super(Institute, self).__init__(request)
        self.institute_list = dacParser.getInstitutes()

    def collection_get(self):
        return self.institute_list

    def get(self):
        institute = [inst for inst in self.institute_list
                     if inst['sigla'].upper() == self.request.matchdict['sigla'].upper()]

        if institute:
            return institute[0]
        else:
            raise KeyError


@resource(**ENDPOINTS['Disciplinas'])
class Subject(ApiResource):

    def collection_get(self):
        institute = self.request.matchdict['instituto'].upper()
        return  dacParser.getSubjects(institute)

    def get(self):
        name = self.request.matchdict['sigla'].upper()
        return dacParser.getSubject(name)


@resource(**ENDPOINTS['Oferecimentos'])
class Offering(ApiResource):

    def collection_get(self):
        data = self.request.matchdict
        return dacParser.getOfferings(data['sigla'].upper(),
                                      self.ano,
                                      self.sem)


    def get(self):

        data = self.request.matchdict
        self.offering = dacParser.getOffering(data['sigla'].upper(),
                                              data['turma'].upper(),
                                              self.ano, self.sem)

        self.enrollments = self.offering.pop('alunos', {})

        return self.offering


@resource(**ENDPOINTS['Matriculados'])
class Enrollments(Offering):

    def get(self):
        super(Enrollments, self).get()
        return self.enrollments
