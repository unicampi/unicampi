import unittest

from unicampi import dacParser

class ParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_institutes(self):
        inst = dacParser.getInstitutes()
        self.assertTrue(len(inst) >  0)

    def test_get_subjects(self):
        inst = dacParser.getSubjects('FEEC')
        self.assertTrue(len(inst) > 0)
    
    def test_get_subjects_ifgw(self):
        inst = dacParser.getSubjects('IFGW')
        self.assertTrue(len(inst) > 0)
        codes = [f['sigla'] for f in inst]
        self.assertIn('F-128', codes)
    
    def test_get_offerings(self):
        inst = dacParser.getOfferings('MC202', '2016', '1')
        self.assertTrue(len(inst) > 0)

    def test_get_offering(self):
        inst = dacParser.getOffering('MC202', 'A', '2016', '1')
        self.assertTrue(len(inst) > 0)
