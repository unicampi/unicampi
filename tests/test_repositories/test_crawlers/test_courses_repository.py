# coding: utf-8

"""Courses Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import CoursesRepository


class CoursesRepositoryTest(TestCase):
    def test_sanity(self):
        i = CoursesRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = CoursesRepository(institute='IC').all()

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_global_fetching_throws_error(self):
        # Courses are dependent of an institute (yet), so calling `.all()`
        # without querying for an institute should throw an error.
        with self.assertRaises(RuntimeError):
            CoursesRepository().all()

    def test_find(self):
        course = CoursesRepository(institute='IC').find(id='MC878')

        self.assertIsNotNone(course)
        self.assertIsInstance(course, dict)
        self.assertEqual(set(course.keys()),
                         {'nome', 'requisitos', 'créditos',
                          'sigla', 'ementa'})
        self.assertEqual(course['nome'], u'Teoria e Aplicações de Grafos')

    def test_find_not_found(self):
        _id = 'non-existent-course'

        with self.assertRaises(KeyError):
            CoursesRepository().filter(institute='IC').find(id=_id)

    def test_filter(self):
        expected = ['MO878', 'MC102']
        courses = (CoursesRepository()
                   .filter(institute='IC', sigla__in=expected)
                   .all())

        for course in courses:
            self.assertIn(course['sigla'], expected)
