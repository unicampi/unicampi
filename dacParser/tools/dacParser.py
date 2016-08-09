#! /bin/python3
# Henrique Noronha Facioli
# Using python3
# This is my first python program
# This module is a parser for DAC Unicamp written in pyhthon. It only gets data
# from dac and should not edit it (for example:generates students mail) - to do
# so, create another file for it and import the functions you want
# Inspired in https://github.com/cacounicamp/gda/
# Por enquanto só funciona com disciplinas da graduação!


import requests                 # To handle http requests - install using pip
import re                       # Regex
import sys                      # To generate
from dacParser.tools.dacParserHelper import *


# url and patterns for getting all the disciplines from unicamp
dacws = "http://www.dac.unicamp.br/"
URL_ALL_INSTITUTES = dacws + 'sistemas/horarios/grad/G2S0/indiceP.htm'
INSTITUTES_CODES_PATTERN = '<font size=-1>([A-Z]*)\s*?<\/font>'
INSTITUTES_NAMES_PATTERN = 'htm\s*?\">(.+?)\s*?<\/a>'

URL_DISCIPLINES = dacws + 'sistemas/horarios/grad/G2S0/%s.htm'
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
VACANCIES_PATTERN = '&nbsp;(\d+) vagas&nbsp;&nbsp;-&nbsp;&nbsp;(\d+) matriculados&nbsp;&nbsp;'
RA_PATTERN = '<td height="18" bgcolor="white" align="center" class="corpo" width="80">([0-9]+)</td>'
NAME_PATTERN = '<td height="18" bgcolor="white" width="270" align="left" class="corpo">&nbsp;&nbsp;&nbsp;&nbsp;(.+)</td>'
COURSE_PATTERN = '<td height="18" bgcolor="white" width="60" align="center" class="corpo">(\d{1,})</td>'
C_TYPE_PATTERN = '<td height="18" bgcolor="white" width="140" align="center" class="corpo">([A-Za-z][A-Za-z ])<\/td>'


# This function returns a list containing all the institutes and it's name
# [('CEL', '	Centro de Ensino de Línguas'),...,...]
def getAllInstitutes():
    # Starts webbrowsin session
    session = requests.Session()

    # Get the webpage
    page = session.get(URL_ALL_INSTITUTES)

    # Get codes and names
    institutes_code = re.findall(INSTITUTES_CODES_PATTERN, page.text)
    institutes_name = re.findall(INSTITUTES_NAMES_PATTERN, page.text)

    allInstitutes = []

    # Creates the list
    for i in range(len(institutes_code)):
        allInstitutes.append((institutes_code[i], institutes_name[i]))

    return allInstitutes


# This function returns the information about an especific subject class
def getDiscipline(discipline, classes, year, semester):
    # Getting a token to check dac page
    # For that, we must keep a session open because expiration
    session = requests.Session()

    # Open token page
    token_page = session.get(DACURL)
    token = token_page.content[1839:1871].decode('ascii')

    # Now, we get the page which contains each of the students in the subject
    # and get Teacher's name, discipline name, and (RA, Students'name)
    page = session.get(URLSUBJECT % (token, semester, year, discipline,
                                     classes))

    # Gets teacher's name removing any escess white space
    teacher = re.findall(PROFESSOR_PATTERN, page.text)
    if not teacher:
        sys.stderr.write("getDiscipline: Turma %s sem professor.\n" %
                         (discipline + classes))
    else:
        teacher = ' '.join(teacher[0].split())

    # Gets discipline code, classes, and name
    discipline_obj = re.findall(DISCIPLINE_PATTERN, page.text)
    if not discipline_obj:
        sys.stderr.write("getDiscipline: Turma %s inválida.\n" % (discipline +
                         classes))
    else:
        # Gets the discipline list = [subject_code, classes, subject_name']
        discipline_obj = discipline_obj[0]
        subject_code = discipline_obj[0]
        classes = discipline_obj[1]
        subject_name = ' '.join(discipline_obj[2].split())

    # Gets registered/vacancies
    discipline_obj = re.findall(VACANCIES_PATTERN, page.text)
    if not discipline_obj:
        sys.stderr.write("getDiscipline: Turma %s 0 vagas.\n" % (discipline +
                         classes))
    else:
        discipline_obj = discipline_obj[0]
        vacancies = discipline_obj[0]
        registered = discipline_obj[1]

    # Gets all the RA and names and join then together, creating a list of
    # tuples [(RA,NAME),...,]
    names = re.findall(NAME_PATTERN, page.text)
    ra_list = re.findall(RA_PATTERN, page.text)
    course = re.findall(COURSE_PATTERN, page.text)

    print(subject_code+classes)

    students = []
    for i in range(len(ra_list)):
        students.append((ra_list[i], names[i].strip(), course[i]))

    # Creates subject object
    subject = Discipline(subject_name, subject_code, classes, year, semester,
                         teacher, vacancies, registered, students)

    return subject


# This function should look on dac webpage and get all the subjects that are
# being offered from institute passade as argument in this semester with it
# classes as:
# [( MC458 , (A,B,C,D) ), (MC040 , (A) ), ... ]
def getAllDisciplines(institute):
    # Start a webbrowsin session
    session = requests.Session()

    # Get the page with all the subjects
    page = session.get(URL_DISCIPLINES % institute)
    disciplines_in_page = re.findall(DISCIPLINE_NAME_PATTERN, page.text)

    offered_disciplines = []
    # Now we go in each subject page and get every classes
    for offered_discipline in disciplines_in_page:
        page = session.get(URL_DISCIPLINE % offered_discipline)
        offered_classes = re.findall(CLASSES_NAME_PATTERN, page.text)
        offered_disciplines.append((offered_discipline, offered_classes))

    return offered_disciplines


# This function gets all the information about all the subjects from institute
# and return it as an array of Subjects
def generateAllDisciplinesFrom(institute):
    subjects = []
    # Get all the offered disciplines
    offered_disciplines = getAllDisciplines(institute)

    # get each of the disciplines offered
    for offered_discipline in offered_disciplines:
        # get each of the classes offered
        for classes in offered_discipline[1]:
            subject = getDiscipline(offered_discipline[0], classes, 2016, 2)
            subjects.append(subject)
    return subjects


# BE CAREFUL
# This function gets all the information from all the subjects of unicamp
# so, it's kind of slow to run it and may take long
# this function return a list of tuples that contains:
# institute_code, list of disciplines
def generateAllDisciplinesUnicamp():
    institutes = getAllInstitutes()
    allDisciplinesUnicamp = []
    for institute in institutes:
        allDisciplinesUnicamp.append((institute[0],
                                     generateAllDisciplinesFrom(institute[0])))
    return allDisciplinesUnicamp


def tests():
    discipline = getDiscipline('MC458', 'A', '2016', '2')
    print(discipline)
    mailList = discipline.generateAcademicEmail
    for mail in mailList:
        print(mail)
