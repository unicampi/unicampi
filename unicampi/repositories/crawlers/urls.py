# coding: utf-8

"""Urls"""

PERIODS = {
    '1': 'G1S0',
    '1e1': 'G1S1',
    '1e2': 'G1S2',
    '1r': 'G5A3',
    '2': 'G2S0',
    '2e1': 'G2S1',
    '2e2': 'G2S2',
    '2r': 'G6A3',
    'fv': 'G5A0',
}

DAC_URL = "http://www.dac.unicamp.br/"

PUBLIC_MENU_URL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'

INSTITUTES_URL = ('http://www.dac.unicamp.br/sistemas/horarios/grad/{term}/'
                  'indiceP.htm')

COURSES_URL = 'http://www.dac.unicamp.br/sistemas/horarios/grad/{term}/{id}.htm'

OFFERINGS_URL = ('http://www.daconline.unicamp.br/altmatr/conspub_situacaovagas'
                 'pordisciplina.do?org.apache.struts.taglib.html.TOKEN={token}&'
                 'cboSubG={term}&cboSubP=0&cboAno={year}&txtDisciplina={course}'
                 '&txtTurma=a&btnAcao=Continuar')

OFFERING_URL = ('http://www.daconline.unicamp.br/altmatr/conspub_matriculados'
                'pordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN={token}&'
                'cboSubG={term}&cboSubP=0&cboAno={year}&txtDisciplina={course}&'
                'txtTurma={id}&btnAcao=Continuar')
