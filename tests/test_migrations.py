import unittest

from api import dacParser


class ParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_institutes(self):
        inst = dacParser.getAllInstitutes()
        self.assertTrue(len(inst) >  0)

    def test_get_disciplines(self):
        inst = dacParser.getAllSubjects('FEEC')
        self.assertTrue(len(inst) > 0)

    def test_get_offerings(self):
        inst = dacParser.getOffering('MC202', 'A', '2016', '1')
        self.assertTrue(len(inst) > 0)
