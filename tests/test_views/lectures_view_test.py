"""Offerings View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import UnicamPI


class LecturesViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(UnicamPI.initiate().app)

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_collection_get(self):
        response = self.app.get('/disciplinas/MC878/periodos/2016s2/turmas',
                                status=200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get(self):
        response = self.app.get('/disciplinas/MC878/periodos/2016s2/turmas/a',
                                status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_not_found(self):
        self.app.get('/disciplinas/MC878iasas/periodos/2016s2/',
                     'turmas/d', expect_errors=True, status=404)

    def test_options(self):
        response = self.app.options(
            '/disciplinas/MC878/periodos/2016s2/turmas', status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_collection_options(self):
        response = self.app.options(
            '/disciplinas/MC878/periodos/2016s2/turmas/a', status=200)
        data = response.json
        self.assertIsInstance(data, dict)
