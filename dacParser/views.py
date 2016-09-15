import html

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from dacParser.tools.dacParser import generateAllSubjectsFrom, getAllInstitutes
from dacParser.tools.dacParserHelper import *
from dacParser.models import Student, Offering, Subject, Teacher, Institute

@login_required
def updatePage(request):
    try:
        allInstitutes = Institute.objects.all().order_by('code')
    except:
        raise Http404("Erro ao parsear institutos")

    results = {
        'institutes': allInstitutes
    }

    return render(request, 'dacParser/update.html', results)


@login_required
def updateInstitutes(request):
    try:
        institutes = getAllInstitutes()
    except:
        raise Http404("Erro ao parsear institutos")

    allInstitutes = []
    for institute in institutes:
        try:
            inst, created = Institute.objects.all().get_or_create(
                code = institute[0],
                name = institute[1],
            )
            allInstitutes.append(inst)
        except:
            raise Http404("Erro ao criar institutos")

    results = {
        'institutes': allInstitutes
    }
    return render(request, 'dacParser/update.html', results)


@login_required
def updateDisciplines(request, institute):
    # First parses all the subjects in this semester
    try:
        print("Parseando disciplinas de "+institute.upper())
        subjects = generateAllSubjectsFrom(institute.upper(), 2016, 2)
        print("Terminou de Parsear disciplinas")
    except:
        print("Erro ao parsear disciplinas")

    # If everything is alright, we hava an array of Subjects
    for subject in subjects:
        # Creats Subject Model
        SubjectModel, created = Subject.objects.all().get_or_create(
            code = subject.code,
            name = subject.name,
            type = subject.type,
        )
        print(subject)

        # Runs the array of offerings in subject
        for off in subject.offerings:
            # Creates Teacher Model
            if off.teacher:
                TeacherModel, created = Teacher.objects.get_or_create(
                    name = off.teacher
                )
            else:
                TeacherModel, created = Teacher.objects.get_or_create(
                    name = 'Sem Professor'
                )
            # Creates discipline Model
            OfferingModel, created = Offering.objects.get_or_create(
                subject = SubjectModel,
                offering_id = off.offering_id,
                year = off.year,
                semester = off.semester,
                teacher = TeacherModel,
                vacancies = off.vacancies,
                registered = off.registered,
            )
            # Now were going to create a Student model and add it to discipline
            # as we add the discipline to the student
            studentsInOffering = off.students
            for student in studentsInOffering:
                StudentModel, created = Student.objects.get_or_create(
                    ra = student.ra,
                    name = html.unescape(student.name),
                    course = student.course,
                    course_type = student.course_modality,
                )
                # Insere a disciplina no aluno
                StudentModel.stu_offerings.add(OfferingModel)
                # Insere o estudante na Disciplina
                OfferingModel.students.add(StudentModel)

    print("Terminamos de gerar informações")

    return HttpResponse("Everything must be ok")
