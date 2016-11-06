from unittest import TestCase

from unicampi.repositories.crawlers.base import OnlineFilter


class OnlineFilterTest(TestCase):
    def setUp(self):
        self.data = [
            {'name': 'jennifer', 'age': 16},
            {'name': 'jane', 'age': 15},
            {'name': 'john', 'age': 12}
        ]

    def test_sanity(self):
        f = OnlineFilter(name='john doe')
        self.assertIsNotNone(f)

    def test_commit_simple_search(self):
        f = OnlineFilter(name='jane')
        result = f.commit(self.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'jane')

    def test_operator_equals(self):
        result = OnlineFilter(name__equals='jennifer').commit(self.data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'jennifer')

    def test_operator_not_equals(self):
        result = OnlineFilter(name__not_equals='jennifer').commit(self.data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'jane')
        self.assertEqual(result[1]['name'], 'john')

    def test_operator_in(self):
        result = OnlineFilter(name__in=['jennifer', 'john']).commit(self.data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'jennifer')
        self.assertEqual(result[1]['name'], 'john')

    def test_operator_contains(self):
        result = OnlineFilter(name__contains='j').commit(self.data)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], 'jennifer')
        self.assertEqual(result[1]['name'], 'jane')
        self.assertEqual(result[2]['name'], 'john')

    def test_operator_not_contains(self):
        result = OnlineFilter(name__not_contains='j').commit(self.data)
        self.assertEqual(len(result), 0)

    def test_invalid_operator_raises_error(self):
        with self.assertRaises(RuntimeError):
            OnlineFilter(name__crazy_operation='jennifer').commit(self.data)
