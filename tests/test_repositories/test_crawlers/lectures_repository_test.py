# coding:utf-8

"""Lectures Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import LecturesRepository


class LecturesRepositoryTest(TestCase):
    def test_sanity(self):
        i = LecturesRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = (LecturesRepository()
                 .filter(year=2016, term=2, course='MC878')
                 .all())

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_global_fetching_throws_error(self):
        # Lectures depend on course and period, so calling `.all()`
        # without querying for these beforehand should throw an error.
        with self.assertRaises(RuntimeError):
            LecturesRepository().all()

    def test_find(self):
        lecture = (LecturesRepository()
                   .filter(year=2016, term=2, course='MC878')
                   .find('a'))

        self.assertIsNotNone(lecture)
        self.assertIsInstance(lecture, dict)
        self.assertEqual(lecture['professor'], 'Christiane Neme Campos')

    def test_find_not_found(self):
        with self.assertRaises(KeyError):
            (LecturesRepository()
             .filter(year=2016, term=2, course='MC878')
             .find(id='non-existent-institute'))
