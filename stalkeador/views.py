from django.shortcuts import render
from django.db.models import Q
from dacParser.models import Student, Offering, Subject, Teacher


# This is the index page (homepage).
# It returns the empty homepage if theres no search_field in the GET request,
# or returns the search query (NEEDS IMPLEMENTATION)
def index(request):
    if request.method == 'GET':
        s_id = request.GET.get('search')
        if(s_id):
            try:
                # https://docs.djangoproject.com/en/1.10/ref/models/querysets/
                # Search for students:
                final_query = Q()
                words = s_id.split()
                for word in words:
                    query = (Q(name__contains=str(word)) |
                             Q(ra__contains=word))
                    final_query = query & final_query
                students = Student.objects.all().filter(final_query).order_by('ra')

                # Searchs offering
                final_query = Q()
                words = s_id.split()
                for word in words:
                    query = (Q(code__contains=str(s_id)) |
                             Q(name__contains=str(s_id)))
                    final_query = query & final_query
                subjects = Subject.objects.all().filter(final_query).order_by('code')

                # Searches Teacher
                query = Q(name__contains=str(s_id))
                teachers = Teacher.objects.all().filter(query).order_by('name')


                results = {
                    'students': students,
                    'subjects': subjects,
                    'teachers': teachers
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

#view for requests on /t/teacherID
#needs to be improved with some kind of id
def teacher(request, teacherID):
    try:
        teacher = Teacher.objects.get(name=teacherID)

        output = {
                'teacher': teacher
        }

        return render(request, 'stalkeador/teacher.html', output)
    except:
        return render(request, 'stalkeador/teacher.html')


# This is for a Discipline page (/s/CODE)
# returns a list containing all the offerings with the code
def subject(request, code, year, semester, offe_id):
    if request.POST:
        print(request.POST)

    try:
        # Always will be about a subject:
        subject = Subject.objects.all().get(
            code = code.upper()
        )
        if offe_id:
            offering = Offering.objects.all().get(
                code = code.upper(),
                year = year,
                semester = semester,
                offering_id = offe_id
            )
            out = {
                'subject': subject,
                'offering': offering,
            }
            # How its the most especif query, it renders the page of the
            # offering
            return render(request, 'stalkeador/offering.html', out)
        elif semester:
            offerings = Offering.objects.all().filter(
                code = code.upper(),
                year = year,
                semester = semester,
            )
        elif offe_id:
            offerings = Offering.objects.all().filter(
                code = code.upper(),
                year = year,
            )
        else:
            offerings = Offering.objects.all().filter(
                code = code.upper(),
            )

        out = {
            'subject': subject,
            'offerings': offerings,
        }
        return render(request, 'stalkeador/subject.html', out)
    except:
        return render(request, 'stalkeador/subject.html')
