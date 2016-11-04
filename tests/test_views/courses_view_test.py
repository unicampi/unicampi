"""Courses View Test"""

from unittest import TestCase

from webtest import TestApp

from unicampi import main


class CoursesViewTest(TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(main({}))

    def test_sanity(self):
        self.assertIsNotNone(self.app)

    def test_collection_get(self):
        response = self.app.get('/institutos/IC/disciplinas', status=200)
        data = response.json
        self.assertIsInstance(data, list)

    def test_get(self):
        response = self.app.get('/disciplinas/MC878', status=200)
        data = response.json
        self.assertIsInstance(data, dict)

    def test_get_not_found(self):
        self.app.get('/disciplinas/mc910910', status=404, expect_errors=True)
