# coding: utf-8
# Crawling patters

# DAC Base URL
DAC_BASE = "http://www.dac.unicamp.br/"

# Institute patters
URL_ALL_INSTITUTES = DAC_BASE + 'sistemas/horarios/grad/G2S0/indiceP.htm'
INSTITUTES_CODES_PATTERN = '<font size=-1>([A-Z]*)\s*?<\/font>'
INSTITUTES_NAMES_PATTERN = 'htm\s*?\">(.+?)\s*?<\/a>'

# Subject patters
URL_SUBJECTS = DAC_BASE + 'sistemas/horarios/grad/G2S0/%s.htm'
URL_DISCIPLINE = DAC_BASE + 'sistemas/horarios/grad/G2S0/%s.htm'
DISCIPLINE_NAME_PATTERN = '[A-Za-z][A-Za-z ][0-9 ]{3}[^<^>]*'
CLASSES_NAME_PATTERN = '([A-Z])\s+\n'

URL_CLASSES = 'http://www.daconline.unicamp.br/altmatr/conspub_situacaovagaspordisciplina.do?org.apache.struts.taglib.html.TOKEN=%s&cboSubG=%s&cboSubP=0&cboAno=%s&txtDisciplina=%s&txtTurma=%s&btnAcao=Continuar'

# urls for listing all the stundents in a discipline
DACURL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'
URLSUBJECT = 'http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN=%s&cboSubG=%s&cboSubP=0&cboAno=%s&txtDisciplina=%s&txtTurma=%s&btnAcao=Continuar'
URLTXT = 'http://www.daconline.unicamp.br/altmatr/fileDownloadPublico.do'

# These are Patterns to extract information from
# www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do
CLASS_PATTERN = '[A-Za-z0-9 ]+</td>'
