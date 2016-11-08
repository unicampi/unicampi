# coding:utf-8

"""Enrollments Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import EnrollmentsRepository


class EnrollmentsRepositoryTest(TestCase):
    def test_sanity(self):
        i = EnrollmentsRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        enrollments = (EnrollmentsRepository()
                       .filter(year='2016', term='2', course='MC878',
                               lecture='a')
                       .all())

        self.assertIsNotNone(enrollments)
        self.assertIsInstance(enrollments, list)
        self.assertGreater(len(enrollments), 0)

    def test_global_fetching_throws_error(self):
        # Enrollments depend on course, lecture and period,
        # so calling `.all()` without querying for these
        # beforehand should throw an error.
        with self.assertRaises(RuntimeError):
            EnrollmentsRepository().all()

    def test_find(self):
        enrollment = (EnrollmentsRepository()
                      .filter(year='2016', term='2', course='MC878',
                              lecture='a')
                      .find(id='117801'))

        self.assertIsNotNone(enrollment)
        self.assertIsInstance(enrollment, dict)
        self.assertEqual(set(enrollment.keys()),
                         {'curso', 'tipo', 'ra', 'nome', 'modalidade'})

    def test_find_not_found(self):
        with self.assertRaises(KeyError):
            (EnrollmentsRepository()
             .filter(year='2016', term='2', course='MC878', lecture='a')
             .find(id='non-existent-institute'))
