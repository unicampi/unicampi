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


# This function returns the information about an especific discipline class ins
# ide a class object
# This returns a tuple, (course, discipline)
def getClass(discipline, classes, year, semester):
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

    # Gets discipline code, classes, and name
    course_parse = re.findall(DISCIPLINE_PATTERN, page.text)

    if not course_parse:
        sys.stderr.write("getDiscipline: Turma %s inválida.\n" % (discipline +
                         classes))
    else:
        # Gets the discipline list = [subject_code, classes, subject_name']
        course_parse = course_parse[0]
        subject_code = course_parse[0]
        class_id = course_parse[1]
        subject_name = ' '.join(course_parse[2].split())
        # Creates the object Course
        course = CourseP(subject_name, subject_code, "U")

    # Gets registered/vacancies
    discipline_parse = re.findall(VACANCIES_PATTERN, page.text)
    if not discipline_parse:
        sys.stderr.write("getDiscipline: Turma %s 0 vagas.\n" % (discipline +
                         classes))
    else:
        discipline_parse = discipline_parse[0]
        vacancies = discipline_parse[0]
        registered = discipline_parse[1]

    # Gets teacher's name removing any escess white space
    teacher = re.findall(PROFESSOR_PATTERN, page.text)
    if not teacher:
        sys.stderr.write("getDiscipline: Turma %s sem professor.\n" %
                         (discipline + classes))
    else:
        teacher = ' '.join(teacher[0].split())

    # Gets all the RA and names and join then together, creating a list of
    # objects students
    names = re.findall(NAME_PATTERN, page.text)
    ra_list = re.findall(RA_PATTERN, page.text)
    school = re.findall(SCHOOL_PATTERN, page.text)

    students = []
    for i in range(len(ra_list)):
        student = StudentP(ra_list[i], names[i], school[i])
        students.append(student)

    # Creates the discipline and add it to the course
    discipline = ClassP(course, class_id, year, semester, teacher, vacancies, registered, students)

    return course, discipline


# This function should look on dac webpage and get all the subjects that are
# being offered from institute passade as argument in this semester with it
# classes as:
# [( MC458 , (A,B,C,D) ), (MC040 , (A) ), ... ]
def getAllCourses(institute):
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


# This function gets all the information about all the courses from institute
# and return it as an array of course
def generateAllCoursesFrom(institute):
    subjects = []
    # Get all the offered disciplines
    offered_disciplines = getAllCourses(institute)

    # get each of the disciplines offered
    for offered_discipline in offered_disciplines:

        # get each of the classes offered
        classes = []
        for classe in offered_discipline[1]:
            course, dis = getClass(offered_discipline[0], classe, 2016, 2)
            classes.append(dis)
        course.classes = classes
        print(course)
        subjects.append(course)


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
    discipline = getClass('MC458', 'A', '2016', '2')
    print(discipline)
