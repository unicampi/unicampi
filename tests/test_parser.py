# encoding: utf8

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
        self.assertIn('F_128', codes)

    def test_get_subject(self):
        inst = dacParser.getSubject('FEEC', 'EA611')
        self.assertEquals(inst['nome'], 'Circuitos II')

    def test_get_subjects_ifgw(self):
        inst = dacParser.getSubject('IFGW', 'F_502')
        self.assertEquals(inst['nome'], 'Eletromagnetismo I')

    def test_get_offerings(self):
        inst = dacParser.getOfferings('MC202', '2016', '1')
        self.assertTrue(len(inst) > 0)

    def test_get_offering(self):
        inst = dacParser.getOffering('MC202', 'A', '2016', '2')
        students = inst.pop('alunos')

        inst_info = {
            "semestre": "2",
            "matriculados": "27",
            "turma": "A",
            "vagas": "25",
            "professor": "Guilherme Pimentel Telles",
            "ano": "2016",
            "sigla": "MC202"
        }
        
        self.assertEquals(len(students), 27)
        self.assertIn('nome', students[17])
        self.assertIn('ra', students[17])
        self.assertDictContainsSubset(inst, inst_info)
