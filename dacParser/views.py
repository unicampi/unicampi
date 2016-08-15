from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dacParser.tools.dacParser import generateAllCoursesFrom
from dacParser.tools.dacParserHelper import *
from dacParser.models import Student, Class, Course, Teacher


@login_required
def updateDisciplines(request, institute):
    # First parses all the classes in this semester
    try:
        print("Parseando disciplinas de "+institute.upper())
        courses = generateAllCoursesFrom(institute.upper())
        print("Terminou de Parsear disciplinas")
    except:
        print("Erro ao parsear disciplinas")

    # If everything is alright, we hava an array of Courses
    for course in courses:
        # Creats Course Model
        CouseModel, created = Course.objects.all().get_or_create(
            code = course.code,
            name = course.name,
            type = course.type,
        )
        print(course)

        # Runs the array of classes in course
        for clas in course.classes:
            # Creates Teacher Model
            if clas.teacher:
                TeacherModel, created = Teacher.objects.get_or_create(
                    name = clas.teacher
                )
            else:
                TeacherModel, created = Teacher.objects.get_or_create(
                    name = 'Sem Professor'
                )
            print(course.code)
            # Creates discipline Model
            ClasseModel, created = Class.objects.get_or_create(
                code = course.code,
                class_id = clas.class_id,
                year = clas.year,
                semester = clas.semester,
                teacher = TeacherModel,
                vacancies = clas.vacancies,
                registered = clas.registered,
            )
            # Now were going to create a Student model and add it to discipline
            # as we add the discipline to the student
            studentsInClass = clas.students
            for student in studentsInClass:
                StudentModel, created = Student.objects.get_or_create(
                    ra = student.ra,
                    name = student.name,
                    school = student.school,
                    course_type = student.course_type,
                )
                # Insere a disciplina no aluno
                StudentModel.disciplines.add(ClasseModel)
                # Insere o estudante na Disciplina
                ClasseModel.students.add(StudentModel)
    print("Terminamos de gerar informações")

    return HttpResponse("Everything must be ok")
