"""Docs View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import UnicamPI


class DocsViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(UnicamPI.initiate().app)

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_get(self):
        response = self.app.get('/', status=200)
        data = response.json
        self.assertIsInstance(data, dict)

        self.assertIn('api_version', data)
        self.assertIn('map', data)
        self.assertIsInstance(data['map'], list)

        for resource in data['map']:
            self.assertIn('name', resource)
            self.assertIn('description', resource)
            self.assertIn('route', resource)
            self.assertIn('_href', resource)
