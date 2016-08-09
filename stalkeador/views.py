from django.shortcuts import render
from django.db.models import Q
from dacParser.models import Student, Discipline


# This is the index page (homepage).
# It returns the empty homepage if theres no search_field in the GET request,
# or returns the search query (NEEDS IMPLEMENTATION)
def index(request):
    if request.method == 'GET':
        s_id = request.GET.get('search')
        if(s_id):
            try:
                # To search for everything, i'm using Q objetc
                # [ https://docs.djangoproject.com/en/1.10/ref/models/querysets/ ]
                # First, looking for students:
                query = Q(name__contains=str(s_id)) | Q(ra=s_id)
                students = Student.objects.all().filter(query)

                query = (Q(code__contains=str(s_id)) |
                            Q(name__contains=str(s_id)))

                disciplines = Discipline.objects.all().filter(query)
                results = {
                    'students': students,
                    'disciplines': disciplines
                    }

                return render(request, 'stalkeador/home-searcher.html', results)
            except:
                print("ERRO: Problema ao realizar busca")
        return render(request, 'stalkeador/home-searcher.html')


# This is for a student page (/s/RA)
# it returns the object student
def student(request, studentRA):
    try:
        student = Student.objects.get(ra=studentRA)
        output = {
            'student': student
        }
        return render(request, 'stalkeador/student.html', output)
    except:
        return render(request, 'stalkeador/student.html')


# This is for a Discipline page (/s/CODE)
# returns a list containing all the disciplines with the code
def discipline(request, code, year, semester, classes):
    try:
        if classes:
            discipline = Discipline.objects.all().get(
                code = code.upper(),
                year = year,
                semester = semester,
                classes = classes
            )
            # How its the most especif query, it renders the page of the
            # discipline
            return render(request, 'stalkeador/discipline.html',
                            {'discipline': discipline})
        elif semester:
            disciplines = Discipline.objects.all().filter(
                code = code.upper(),
                year = year,
                semester = semester,
            )
        elif classes:
            disciplines = Discipline.objects.all().filter(
                code = code.upper(),
                year = year,
            )
        else:
            disciplines = Discipline.objects.all().filter(
                code = code.upper(),
            )

        out = {
            'disciplines': disciplines
        }
        return render(request, 'stalkeador/disciplines.html', out)
    except:
        return render(request, 'stalkeador/disciplines.html')
