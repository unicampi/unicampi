# Henrique Noronha Facioli
# Using python3
# These are the urls and regex for pasring dac


# url and patterns for getting all the disciplines from unicamp
dacws = "http://www.dac.unicamp.br/"
URL_ALL_INSTITUTES = dacws + 'sistemas/horarios/grad/G2S0/indiceP.htm'
INSTITUTES_CODES_PATTERN = '<font size=-1>([A-Z]*)\s*?<\/font>'
INSTITUTES_NAMES_PATTERN = 'htm\s*?\">(.+?)\s*?<\/a>'

URL_SUBJECTS = dacws + 'sistemas/horarios/grad/G2S0/%s.htm'
URL_DISCIPLINE = dacws + 'sistemas/horarios/grad/G2S0/%s.htm'
EMMENT = '<font face="Arial,Helvetica"><font size=-1>(?P<emenda>.+)</font></font></td>'
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

# This is the object thar stores a subjcect information
class SubjectP(object):
    name = ""
    code = ""
    type = ""   # undergrad or grad
    offerings = []    # an array of Class

    def __init__(self, name, code, type, offerings):
        self.name = name
        self.code = code
        self.type = type
        self.offerings = offerings

    # TO help on debug and kind of pretty
    def __str__(self):
        beautiprint = '''
        Name        : %s
        Code        : %s
        Type        : %s
        # Offerings : %s
        '''
        return (beautiprint %
                (self.name, self.code, self.type,str(len(self.offerings))))

    def __eq__(self, other):
        return self.code == other.code


class OfferingP(object):
    subject = object
    offering_id = ""
    semester = ""
    year = ""
    teacher = ""
    vacancies = 0
    registered = 0
    students = object


    def __init__(self, subject, offering_id, year, semester, teacher, vacancies,
                 registered, students):
        self.subject = subject
        self.year = year
        self.semester = semester
        self.offering_id = offering_id
        self.teacher = teacher
        self.vacancies = vacancies
        self.registered = registered
        self.students = students

    def __str__(self):
        beautiprint = '''
        Offering ID : %s
        Year        : %s
        Semester    : %s
        Teacher     : %s
        Regis/Vacan : %s/%s
        '''
        return (beautiprint %
                (self.offering_id, self.year, self.semester, self.teacher,
                 self.registered, self.vacancies))


class StudentP(object):
    ra = ""
    name = ""
    type = ""
    course = ""
    course_modality = ""

    def __init__(self, ra, name, course, type, course_modality):
        self.ra = ra
        self.name = name
        self.course = course
        self.type = type
        self.course_modality = course_modality

    def __str__(self):
        return (self.ra + ' ' + self.name + ' - ' + self.course + ' ' +
                self.course_modality)
