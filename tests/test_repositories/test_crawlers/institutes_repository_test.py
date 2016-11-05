# coding:utf-8

"""Institutes Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import InstitutesRepository


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

        self.assertDictEqual(i1.query, i2.query)

    def test_filter(self):
        expected = ['IC', 'IFCH']
        institutes = InstitutesRepository().filter(sigla__in=expected).all()
        self.assertEqual(len(institutes), len(expected))

    def test_filter_on_initialization(self):
        expected = ['IC', 'IFCH']
        institutes = InstitutesRepository(sigla__in=expected).all()
        self.assertEqual(len(institutes), len(expected))

    def test_where(self):
        expected = ['IC', 'IFCH']
        institutes = InstitutesRepository().where(sigla__in=expected)
        self.assertEqual(len(institutes), len(expected))
