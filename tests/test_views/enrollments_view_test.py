"""Enrollments View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import UnicamPI


class EnrollmentsViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(UnicamPI.initiate().app)

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_collection_get(self):
        response = self.app.get('/periodos/2016s2/oferecimentos/MC878'
                                '/turmas/a/matriculados',
                                status=200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get(self):
        response = self.app.get('/periodos/2016s2/oferecimentos/MC878'
                                '/turmas/a/matriculados/117801',
                                status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_not_found(self):
        self.app.get('/periodos/2016s2/oferecimentos/MC878'
                     '/turmas/a/matriculados/188972',
                     status=404, expect_errors=True)

    def test_options(self):
        response = self.app.options('/periodos/2016s2/oferecimentos/MC878'
                                    '/turmas/a/matriculados', status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_collection_options(self):
        response = self.app.options('/periodos/2016s2/oferecimentos/MC878'
                                    '/turmas/a/matriculados/117801',
                                    status=200)
        data = response.json
        self.assertIsInstance(data, dict)
