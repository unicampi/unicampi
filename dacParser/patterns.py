# url and patterns for getting all the disciplines from unicamp
dacws = "http://www.dac.unicamp.br/"
URL_ALL_INSTITUTES = dacws + 'sistemas/horarios/grad/G2S0/indiceP.htm'
INSTITUTES_CODES_PATTERN = '<font size=-1>([A-Z]*)\s*?<\/font>'
INSTITUTES_NAMES_PATTERN = 'htm\s*?\">(.+?)\s*?<\/a>'

URL_SUBJECTS = dacws + 'sistemas/horarios/grad/G2S0/%s.htm'
URL_DISCIPLINE = dacws + 'sistemas/horarios/grad/G2S0/%s.htm'
DISCIPLINE_NAME_PATTERN = '[A-Za-z][A-Za-z ][0-9]{3}(?= )'
CLASSES_NAME_PATTERN = '([A-Z])\s+\n'

# urls for listing all the stundents in a discipline
DACURL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'
URLSUBJECT = 'http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN=%s&cboSubG=%s&cboSubP=0&cboAno=%s&txtDisciplina=%s&txtTurma=%s&btnAcao=Continuar'
URLTXT = 'http://www.daconline.unicamp.br/altmatr/fileDownloadPublico.do'

# These are Patterns to extract information from
# www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do
PROFESSOR_PATTERN = 'Docente:</span>&nbsp;&nbsp;(?P<professor>.+)</td>'
DISCIPLINE_PATTERN = 'Disciplina:</span>&nbsp;&nbsp;(?P<disciplina>[A-Za-z][A-Za-z ][0-9]{3}) (?P<turma>[A-Za-z0-9]) &nbsp;&nbsp; -&nbsp;&nbsp; (?P<materia>.+)</td>'
TYPE_DISCIPLINE_PA = '<tr height="18">											<td bgcolor="#f2f2f2" class="corpo" height="18">&nbsp;&nbsp; <span class="itemtabela">N&iacute;vel:<\/span>&nbsp;&nbsp;(\w+)<\/td>										<\/tr>'
VACANCIES_PATTERN = '&nbsp;(\d+) vagas&nbsp;&nbsp;-&nbsp;&nbsp;(\d+) matriculados&nbsp;&nbsp;'
STUDENT_PATTERN = ''

RA_PATTERN = '<td height="18" bgcolor="white" align="center" class="corpo" width="80">([0-9]+)</td>'
NAME_PATTERN = '<td height="18" bgcolor="white" width="270" align="left" class="corpo">&nbsp;&nbsp;&nbsp;&nbsp;(.+)</td>'
SCHOOL_PATTERN = '<td height="18" bgcolor="white" width="60" align="center" class="corpo">(\d{1,})</td>'
C_TYPE_PATTERN = '<td height="18" bgcolor="white" width="140" align="center" class="corpo">([A-Za-z][A-Za-z ])<\/td>'

STUDENT_PATTERN = '<td height="18" bgcolor="white" align="center" class="corpo" width="30">36</td>\n\t\t\t\t\t\t\t\t\t<td height="18" bgcolor="white" align="center" class="corpo" width="80">(?P<ra>[0-9]+)</td>\n\t\t\t\t\t\t\t\t\t<td height="18" bgcolor="white" width="270" align="left" class="corpo">&nbsp;&nbsp;&nbsp;&nbsp;(?P<nome>.+)</td>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t   <td height="18" bgcolor="white" width="60" align="center" class="corpo">(?P<school>\d{1,})</td>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<td height="18" bgcolor="white" width="60" align="center" class="corpo">G</td>\n\t\t\t\t\t\t\t\t\t<td height="18" bgcolor="white" width="140" align="center" class="corpo">(?P<coursetype>[A-Za-z][A-Za-z ])</td>\n\t\t\t\t\t\t\t\t</tr>'

STUDENT_TYPE = ('<td height="18" bgcolor="white" width="60" align="center" class="corpo">(.+)<\/td>\n'+
        '									<td height="18" bgcolor="white" width="140" align="center" class="corpo">(.+)?<\/td>')

