# coding: utf-8

"""Courses Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import ActiveCoursesRepository


class ActiveCoursesRepositoryTest(TestCase):

    def test_sanity(self):
        i = ActiveCoursesRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = ActiveCoursesRepository(term=2, institute='IC').all()

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_global_fetching_throws_error(self):
        # Courses are dependent of an institute (yet), so calling `.all()`
        # without querying for an institute should throw an error.
        with self.assertRaises(RuntimeError):
            ActiveCoursesRepository().all()

    def test_find(self):
        course = ActiveCoursesRepository(term=2, institute='IC').find(id='MC878')

        self.assertIsNotNone(course)
        self.assertIsInstance(course, dict)
        self.assertEqual(set(course.keys()),
                         {'nome', 'requisitos', 'creditos',
                          'sigla', 'ementa', 'turmas'})
        self.assertEqual(course['nome'], u'Teoria e Aplicações de Grafos')
        self.assertIsInstance(course['requisitos'], list)
        self.assertEqual(course['turmas'][0]['turma'], 'A')

    def test_find_not_found(self):
        _id = 'non-existent-course'

        with self.assertRaises(KeyError):
            ActiveCoursesRepository(term=2).filter(institute='IC').find(id=_id)

    def test_filter(self):
        expected = ['MO878', 'MC102']
        courses = (ActiveCoursesRepository(term=2)
                   .filter(institute='IC', sigla__in=expected)
                   .all())

        for course in courses:
            self.assertIn(course['sigla'], expected)
