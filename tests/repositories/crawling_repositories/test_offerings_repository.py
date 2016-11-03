# coding:utf-8

from unittest import TestCase

from unicampi.repositories.crawling_repositories import OfferingsRepository


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
