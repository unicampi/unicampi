# coding:utf-8

"""Institutes Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import ActiveInstitutesRepository


class ActiveInstitutesRepositoryTest(TestCase):
    def test_sanity(self):
        i = ActiveInstitutesRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = ActiveInstitutesRepository(term=2).all()

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_find(self):
        institute = ActiveInstitutesRepository(term=2).find(id='IC')

        self.assertIsNotNone(institute)
        self.assertIsInstance(institute, dict)
        self.assertDictEqual(institute, {
            'sigla': 'IC',
            'nome': u'Instituto de Computação'
        })

    def test_find_not_found(self):
        _id = 'non-existent-institute'

        with self.assertRaises(KeyError):
            ActiveInstitutesRepository(term=2).find(id=_id)

    def test_filter_equals_local_initiation(self):
        i1 = ActiveInstitutesRepository(term=2, name__in=['IC', 'FEEC'])
        i2 = ActiveInstitutesRepository(term=2).filter(name__in=['IC', 'FEEC'])

        self.assertDictEqual(i1.query, i2.query)

    def test_filter(self):
        expected = ['IC', 'IFCH']
        institutes = ActiveInstitutesRepository(term=2).filter(sigla__in=expected).all()
        self.assertEqual(len(institutes), len(expected))

    def test_filter_on_initialization(self):
        expected = ['IC', 'IFCH']
        institutes = ActiveInstitutesRepository(term=2, sigla__in=expected).all()
        self.assertEqual(len(institutes), len(expected))

    def test_where(self):
        expected = ['IC', 'IFCH']
        institutes = ActiveInstitutesRepository(term=2).where(sigla__in=expected)
        self.assertEqual(len(institutes), len(expected))
