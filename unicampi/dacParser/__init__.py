# coding: utf-8
from __future__ import unicode_literals

import requests
import re
from bs4 import BeautifulSoup

from .patterns import *
from .utils import ContentFinder

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

    token_page = session.get(DACURL)
    token = token_page.content[1839:1871].decode('ascii')

    page = session.get(URLSUBJECT % (token, semester, year, subject, cls))

    soup = BeautifulSoup(page.text, 'lxml')
    tds = soup.find_all('table')

    # Get table 6 (general info)
    data = tds[6]

    finder = ContentFinder(data.text)

    teacher = finder.find_by_content('Docente:').split(':', 1)[1].strip()
    situation = finder.find_by_content('Situação:').split(':', 1)[1].strip()

    # Data is type "Situação:  25 vagas  -  12 matriculados" 
    vacancy, registered = situation.split('-')

    vacancies = vacancy.strip().split(' ', 1)[0]
    registered = registered.strip().split(' ', 1)[0]

    # Get table 8 (students)
    students_data = tds[8].find_all('td')

    # Remove heder
    students_data = [s.text for s in students_data[7:]]

    students = []
    for i in range(0, len(students_data), 6):
        students.append({
            'ra': students_data[i+1],
            'nome': students_data[i+2].strip(),
            'curso': students_data[i+3],
            'tipo': students_data[i+4],
            'modalidade': students_data[i+5],
        })

    offering = {
        'sigla': subject,
        'turma': cls,
        'ano': year,
        'semestre': semester,
        'professor': teacher,
        'vagas': vacancies,
        'matriculados': registered,
        'alunos': students
    }

    return offering


def getSubjects(institute):

    session = requests.Session()

    page = session.get(URL_SUBJECTS % institute)

    soup = BeautifulSoup(page.text, 'lxml')
    tds = soup.find_all('table')

    data = tds[1].find_all('td')
    # strip and remove raw content
    data = [el.text.strip() for el in data[1:]]

    subjects = []
    for sub in data:

        code = sub[:5]
        name = sub[5:]

        subjects.append({
            'nome' : name.strip(),
            'sigla': code.replace(' ', '_'),
        })

    return subjects


def getSubject(institute, code):

    session = requests.Session()

    page = session.get(URL_DISCIPLINE % code)

    soup = BeautifulSoup(page.text, 'lxml')
    tds = soup.find_all('table')

    data = tds[1].find_all('td')[1]

    finder = ContentFinder(data.text)

    main_info = finder.splited[0]
    code = main_info[:5]
    name = main_info[5:].strip()

    content = finder.find_by_content('Ementa:', offset=1)
    credits = finder.find_by_content('Créditos:', offset=0)[-3:]
    requires_list = finder.find_by_content('Pré-Requisitos:', offset=1,
                                           end_pattern='Turma:')

    req_dates = requires_list[::2]
    req_values = requires_list[1::2]

    # split 'or' requirements
    req_values = [v.strip().split(' / ') for v in req_values]

    # split 'and' requirements
    for i in range(len(req_values)):
        req_values[i] = [v.strip().split('  ') for v in req_values[i]]

    requires = dict(zip(req_dates, req_values))

    return {
        'nome' : name,
        'sigla': code.replace(' ', '_'),
        'ementa': content,
        'pré-requisitos': requires,
        'créditos': int(credits),
    }
