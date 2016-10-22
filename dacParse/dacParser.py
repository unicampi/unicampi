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
from bs4 import BeautifulSoup
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
# This returns a tuple, (subject, discipline)
def getOffering(discipline, offerings, year, semester):
    # Getting a token to check dac page
    # For that, we must keep a session open because expiration
    session = requests.Session()

    # Open token page
    token_page = session.get(DACURL)
    token = token_page.content[1839:1871].decode('ascii')

    # Now, we get the page which contains each of the students in the subject
    # and get Teacher's name, discipline name, and (RA, Students'name)
    page = session.get(URLSUBJECT % (token, semester, year, discipline,
                                     offerings))

    # Gets discipline code, offerings, and name
    subject_parse = re.findall(DISCIPLINE_PATTERN, page.text)

    if not subject_parse:
        sys.stderr.write("getDiscipline: Turma %s inválida.\n" % (discipline +
                         offerings))
    else:
        # Gets the discipline list = [subject_code, offerings, subject_name']
        subject_parse = subject_parse[0]
        subject_code = subject_parse[0]
        offering_id = subject_parse[1]
        subject_name = ' '.join(subject_parse[2].split())
        # Creates the object Subject
        subject = SubjectP(subject_name, subject_code, "U", [])

    # Gets registered/vacancies
    discipline_parse = re.findall(VACANCIES_PATTERN, page.text)
    if not discipline_parse:
        sys.stderr.write("getDiscipline: Turma %s 0 vagas.\n" % (discipline +
                         offerings))
    else:
        discipline_parse = discipline_parse[0]
        vacancies = discipline_parse[0]
        registered = discipline_parse[1]

    # Gets teacher's name removing any escess white space
    teacher = re.findall(PROFESSOR_PATTERN, page.text)
    if teacher:
        teacher = ' '.join(teacher[0].split())

    # Gets all the RA and names and join then together, creating a list of
    # objects students
    soup = BeautifulSoup(page.text, 'lxml')

    students = []
    print(discipline+offerings)

    if int(registered) != 0:
        # Get the 8th table on the page as it contains the students
        table = soup.find_all('table')[8]
            # Runs all the trs (lines on the table)
        for trs in table.find_all('tr')[2:]:
            tds = trs.find_all('td')
            student = StudentP(tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text)

            students.append(student)
    else:
        print('Sem alunos')


    discipline = OfferingP(subject, offering_id, year, semester, teacher, vacancies,
                        registered, students)
    subject.offerings.append(discipline)

    return subject, discipline


# This function should look on dac webpage and get all the subjects that are
# being offered from institute passade as argument in this semester with it
# offerings as:
# [( MC458 , (A,B,C,D) ), (MC040 , (A) ), ... ]
def getAllSubjects(institute):
    # Start a webbrowsin session
    session = requests.Session()

    # Get the page with all the subjects
    page = session.get(URL_SUBJECTS % institute)

    disciplines_in_page = re.findall(DISCIPLINE_NAME_PATTERN, page.text)

    offered_disciplines = []
    # Now we go in each subject page and get e8very offerings
    for offered_discipline in disciplines_in_page:
        page = session.get(URL_DISCIPLINE % offered_discipline)

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')
        # This is emment text
        emment = tds[2].find_all('td')[1].text
        offered_offerings = re.findall(CLASSES_NAME_PATTERN, page.text)
        offered_disciplines.append([offered_discipline, offered_offerings, emment])

    return offered_disciplines


# This function gets all the information about all the subjects from institute
# and return it as an array of subject
def generateAllSubjectsFrom(institute, year, sem):
    subjects = []
    # Get all the offered disciplines
    offered_disciplines = getAllSubjects(institute)

    # get each of the disciplines offered
    for offered_discipline in offered_disciplines:

        # get each of the offerings offered
        offerings = []
        for classe in offered_discipline[1]:
            subject, dis = getOffering(offered_discipline[0], classe, year, sem)
            offerings.append(dis)
        subject.offerings = offerings
        subject.emment = offered_discipline[2]
        print(subject)
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
    subject, discipline = getOffering('MC001', 'A', '2016', '2')
    print(subject)
    print(discipline)
    for student in discipline.students:
        print(student)
