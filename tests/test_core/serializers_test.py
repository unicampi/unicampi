from unittest import TestCase

from unicampi.core.serializers import Serializer


class SerializerTest(TestCase):
    def test_sanity(self):
        s = Serializer({}, None)
        self.assertIsNotNone(s)

    def test_parse(self):
        data = dict(
            id='1023',
            name='john doe',
            age='26',
            occupation='software engineer',
        )
        schema = dict(
            id={'type': int, 'preprocess': lambda x: x + 20},
            name={'type': str, 'preprocess': 'uppercase'},
            age={'type': int},
        )

        s = Serializer(data, schema)

        self.assertEqual(type(s['id']), int)
        self.assertEqual(s['id'], 1043)

        self.assertEqual(type(s['age']), int)
        self.assertEqual(s['age'], 26)

        self.assertEqual(s['name'], 'JOHN DOE')
        self.assertEqual(s['occupation'], 'software engineer')

    def test_unknown_preprocess_raises_error(self):
        data = dict(
            id='1023',
            name='john doe',
            age='26',
            occupation='software engineer',
        )
        schema = dict(
            name={'type': str, 'preprocess': 'unknown-pre-process'},
            age={'type': int},
        )

        with self.assertRaises(KeyError):
            Serializer(data, schema)
