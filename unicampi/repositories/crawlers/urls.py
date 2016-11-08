# coding: utf-8

"""Urls"""

PERIODS = {
    '1': 'G1S0',
    '1esp1': 'G1S1',
    '1esp2': 'G1S2',
    '1rec': 'G5A3',
    '2': 'G2S0',
    '2esp1': 'G2S1',
    '2esp2': 'G2S2',
    '2rec': 'G6A3',
    'f': 'G5A0',
}

DAC_URL = "http://www.dac.unicamp.br/"

PUBLIC_MENU_URL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'

INSTITUTES_URL = ('http://www.dac.unicamp.br/sistemas/horarios/grad/{term}/'
                  'indiceP.htm')

COURSES_URL = 'http://www.dac.unicamp.br/sistemas/horarios/grad/{term}/{id}.htm'

LECTURES_URL = ('http://www.daconline.unicamp.br/altmatr/conspub_situacaovagas'
                'pordisciplina.do?org.apache.struts.taglib.html.TOKEN={token}&'
                'cboSubG={term}&cboSubP=0&cboAno={year}&txtDisciplina={course}'
                '&txtTurma=a&btnAcao=Continuar')

LECTURE_URL = ('http://www.daconline.unicamp.br/altmatr/conspub_matriculados'
               'pordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN={token}&'
               'cboSubG={term}&cboSubP=0&cboAno={year}&txtDisciplina={course}&'
               'txtTurma={id}&btnAcao=Continuar')
