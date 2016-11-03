# coding:utf-8

from unittest import TestCase

from unicampi.repositories.crawling_repositories import InstitutesRepository


class InstitutesRepositoryTest(TestCase):
    def test_sanity(self):
        i = InstitutesRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = InstitutesRepository().all()

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_find(self):
        institute = InstitutesRepository().find(id='IC')

        self.assertIsNotNone(institute)
        self.assertIsInstance(institute, dict)
        self.assertDictEqual(institute, {
            'sigla': 'IC',
            'nome': u'Instituto de Computação'
        })

    def test_find_not_found(self):
        _id = 'non-existent-institute'

        with self.assertRaises(KeyError):
            InstitutesRepository().find(id=_id)

    def test_filter_equals_local_initiation(self):
        i1 = InstitutesRepository(name__in=['IC', 'FEEC'])
        i2 = InstitutesRepository().filter(name__in=['IC', 'FEEC'])

        self.assertDictEqual(i1.matching, i2.matching)

    def test_filter(self):
        with self.assertRaises(NotImplementedError):
            InstitutesRepository().filter(sigla__in=['IC', 'IFCH']).all()

    def test_query(self):
        with self.assertRaises(NotImplementedError):
            InstitutesRepository().query(sigla__in=['IC', 'FEEC'])
