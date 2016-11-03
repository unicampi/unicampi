# coding:utf-8

"""Offerings Repository Test"""

from unittest import TestCase

from unicampi.repositories.crawlers import OfferingsRepository


class OfferingsRepositoryTest(TestCase):
    def test_sanity(self):
        i = OfferingsRepository()
        self.assertIsNotNone(i)

    def test_all(self):
        items = (OfferingsRepository()
                 .filter(year=2016, term=2, course='MC878')
                 .all())

        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

    def test_global_fetching_throws_error(self):
        # Offerings depend on course and period, so calling `.all()`
        # without querying for these beforehand should throw an error.
        with self.assertRaises(RuntimeError):
            OfferingsRepository().all()

    def test_find(self):
        offering = (OfferingsRepository()
                    .filter(year=2016, term=2, course='MC878')
                    .find('a'))

        self.assertIsNotNone(offering)
        self.assertIsInstance(offering, dict)
        self.assertEqual(offering['professor'], 'Christiane Neme Campos')

    def test_find_not_found(self):
        with self.assertRaises(KeyError):
            (OfferingsRepository()
             .filter(year=2016, term=2, course='MC878')
             .find(id='non-existent-institute'))
