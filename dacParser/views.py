from django.http import HttpResponse
from dacParser.dacParser import generateAllDisciplinesFrom
from dacParser.models import Student, Discipline, Teacher


def updateDisciplines(request):
    print("Parseando disciplinas")
    # Por enquanto esotu testanto somente com disciplinas do IC
    # Pode-se usar as outras funções do dacParser
    disciplines = generateAllDisciplinesFrom('IC')
    print("Terminou de Parsear disciplinas")

    for discipline in disciplines:
        # Creates Teacher Model
        TeacherModel, created = Teacher.objects.get_or_create(
            name = discipline.teacher
        )

        # Creates discipline Model
        DisciplineModel, created = Discipline.objects.get_or_create(
            name = discipline.name,
            code = discipline.code,
            year = discipline.year,
            teacher = TeacherModel,
            classes = discipline.classes,
            semester = discipline.semester,
            vacancies = discipline.vacancies,
            registered = discipline.registered,
        )
        # Now we're going to create a Student model and add it to discipline
        # as we are going to add the discipline to the student
        studentsInDiscipline = discipline.students
        for studentInDis in studentsInDiscipline:
            StudentModel, created = Student.objects.get_or_create(
                ra = studentInDis[0],
                name = studentInDis[1],
            )
            # Insere a disciplina no aluno
            StudentModel.disciplines.add(DisciplineModel)
            # Insere o estudante na Disciplina
            DisciplineModel.students.add(StudentModel)
    print("Terminamos de gerar informações")

    return HttpResponse("Everything must be ok")
