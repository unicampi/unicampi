# -- coding: utf-8 --

from unittest import TestCase

from unicampi.repositories.crawling_repositories import CoursesRepository


class CoursesRepositoryTest(TestCase):
    def test_sanity(self):
        i = CoursesRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = CoursesRepository(institute='IC').all()

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_all_global_fetching(self):
        with self.assertRaises(NotImplementedError):
            CoursesRepository().all()

    def test_find(self):
        course = CoursesRepository(institute='IC').find(id='MC878')

        self.assertIsNotNone(course)
        self.assertIsInstance(course, dict)
        self.assertEqual(set(course.keys()),
                         {'nome', 'pré-requisitos', 'créditos', 'sigla',
                          'ementa'})
        self.assertEqual(course['nome'], u'Teoria e Aplicações de Grafos')

    def test_find_not_found(self):
        _id = 'non-existent-course'

        with self.assertRaises(KeyError):
            CoursesRepository().filter(institute='IC').find(id=_id)

    def test_filter(self):
        with self.assertRaises(NotImplementedError):
            CoursesRepository().filter(sigla={'$in': ['IC', 'IFCH']}).all()

    def test_query(self):
        with self.assertRaises(NotImplementedError):
            CoursesRepository().query(sigla={'$in': ['IC', 'FEEC']})
