"""Enrollments View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import main


class EnrollmentsViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(main({}))

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_collection_get(self):
        response = self.app.get('/periodos/2016s2/oferecimentos/MC878'
                                '/turma/a/matriculados',
                                status=200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get(self):
        response = self.app.get('/periodos/2016s2/oferecimentos/MC878'
                                '/turma/a/matriculados/117801',
                                status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_not_found(self):
        self.app.get('/periodos/2016s2/oferecimentos/MC878'
                     '/turma/a/matriculados/188972',
                     status=404, expect_errors=True)
