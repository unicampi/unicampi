"""Offerings View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import main


class OfferingsViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(main({}))

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_collection_get(self):
        response = self.app.get('/periodos/2016s2/oferecimentos/MC878',
                                status=200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get(self):
        response = self.app.get('/periodos/2016s2/oferecimentos/MC878'
                                '/turma/a',
                                status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_not_found(self):
        self.app.get('/periodos/2016s2/oferecimentos/MC8cdsas8/'
                     'turma/d', expect_errors=True, status=404)
