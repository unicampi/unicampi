# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup

from .patterns import *


def getInstitutes():
    
    session = requests.Session()
    page = session.get(URL_ALL_INSTITUTES)

    # Get codes and names
    institutes_code = re.findall(INSTITUTES_CODES_PATTERN, page.text)
    institutes_name = re.findall(INSTITUTES_NAMES_PATTERN, page.text)

    allInstitutes = []

    # Creates the list
    for i in range(len(institutes_code)):
        allInstitutes.append({
            "sigla": institutes_code[i],
            "nome": institutes_name[i],
        })

    return allInstitutes

def getOfferings(subject, year, semester):

    session = requests.Session()

    # Open token page
    token_page = session.get(DACURL)
    token = token_page.content[1839:1871].decode('ascii')

    page = session.get(URL_CLASSES % (token, semester, year, subject, 'a'))
    
    subject_parse = re.findall(CLASS_PATTERN, page.text)[3:]

    offs = []
    for i in range(int(len(subject_parse)/3)):
        offs.append({
            'turma': subject_parse[3*i].split('<')[0].strip(),
            'vagas': subject_parse[3*i+1].split('<')[0].strip(),
            'matriculados': subject_parse[3*i+2].split('<')[0].strip(),
        })
    return offs


def getOffering(subject, cls, year, semester):
    
    session = requests.Session()

    # Open token page
    token_page = session.get(DACURL)
    token = token_page.content[1839:1871].decode('ascii')

    page = session.get(URLSUBJECT % (token, semester, year, subject, cls))

    # Gets subject code, offerings, and name
    subject_parse = re.findall(DISCIPLINE_PATTERN, page.text)

    if not subject_parse:
        raise ValueError
    else:
        # Gets the subject list = [subject_code, offerings, subject_name']
        subject_parse = subject_parse[0]
        subject_code = subject_parse[0]
        offering_id = subject_parse[1]
        subject_name = ' '.join(subject_parse[2].split())

    # Gets registered/vacancies
    subject_parse = re.findall(VACANCIES_PATTERN, page.text)
    if not subject_parse:
        pass
    else:
        subject_parse = subject_parse[0]
        vacancies = subject_parse[0]
        registered = subject_parse[1]

    # Gets teacher's name removing any escess white space
    teacher = re.findall(PROFESSOR_PATTERN, page.text)
    if teacher:
        teacher = ' '.join(teacher[0].split())

    # Gets all the RA and names and join then together, creating a list of
    # objects students
    soup = BeautifulSoup(page.text, 'lxml')

    students = []

    if int(registered) != 0:
        # Get the 8th table on the page as it contains the students
        table = soup.find_all('table')[8]
            # Runs all the trs (lines on the table)
        for trs in table.find_all('tr')[2:]:
            tds = trs.find_all('td')
            student = {
                'ra': tds[1].text, 
                'nome': tds[2].text.strip(),
                'curso': tds[3].text.strip(),
                'tipo': tds[4].text,
                'modalidade': tds[5].text.strip()
            }

            students.append(student)

    offering = {
        'sigla': subject,
        'turma': offering_id,
        'ano': year,
        'semestre': semester,
        'professor': teacher,
        'vagas': vacancies,
        'matriculados': registered,
        'alunos': students
    }
    
    return offering


def getSubjects(institute):
    # Start a webbrowsin session
    session = requests.Session()

    # Get the page with all the subjects
    page = session.get(URL_SUBJECTS % institute)

    subjects_in_page = re.findall(DISCIPLINE_NAME_PATTERN, page.text)
    subjects_in_page = [sub for sub in subjects_in_page if not sub.endswith('.htm"')]

    offered_subjects = []
    
    # Now we go in each subject page and get e8very offerings
    for offered_subject in subjects_in_page:

        code = offered_subject.strip()[:5]
        name = offered_subject.strip()[5:]
        page = session.get(URL_DISCIPLINE % code)

        soup = BeautifulSoup(page.text, 'lxml')
        tds = soup.find_all('table')
        # This is emment text
        try:
            emment = tds[2].find_all('td')[1].text
        except IndexError:
            emment = ''

        offered_subjects.append({
            'nome' : name.strip(),
            'sigla': code.replace(' ', '-'), 
            'ementa': emment.strip()
        })

    return offered_subjects


