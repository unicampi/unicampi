from django.shortcuts import render
from django.http import Http404
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from dacParser.models import Class, Student
from gda.models import Token

URL = 'http://127.0.0.1:8000/'
FROM_EMAIL = 'GDA TESTER <gdatester@gmail.com>'


# Generates tokens for all the students from a discipline
@login_required
def generateTokens(request, code, year, semester, classes):
    try:
        # First, gets detials about discipline
        discipline = Class.objects.all().get(
            code = code.upper(),
            year = year,
            semester = semester,
            class_id = classes
        )
    except Class.DoesNotExist:
        raise Http404("Não encontrou a materia desejada")

    # Generate a token per student
    try:
        students_ok = []
        for student in discipline.students.all():
            token, created = Token.objects.all().get_or_create(
                student = student,
                discipline = discipline
            )
            students_ok.append(token.student)

        out = {
            'students': students_ok
        }
    except:
        raise Http404("Não foi possivel gerar token")

    return render(request, 'gda/generate.html', out)


# Send email for all the students in a class
@login_required
def sendMail(request, code, year, semester, classes):
    try:
        # First, gets class
        discipline = Class.objects.all().get(
            code = code.upper(),
            year = year,
            semester = semester,
            class_id = classes
        )
    except Class.DoesNotExist:
        raise Http404("Não encontrou a materia desejada")
    # Find's all the tokens that is from this class
    try:
        tokens = Token.objects.all().filter(
            discipline = discipline
        )
        print(tokens.all())
    except:
        raise Http404("Não encontrou a materia desejada")

    try:
        # Now we generate an email for each student in the discipline
        for token in tokens.all():
            header = '[GDA][%s] Avaliação da matéria %s' % (discipline.code,
                                                            discipline)
            link = URL + 'vote' + str(discipline.url()) + '/' + str(token.token)
            message = 'Olá, essa é uma mensagem automatica para envio do link de votação do GDA. \nO link para sua votação é: %s\n\n O link é a unica maneira de votar, então guarde secretamente o seu link <3' % link

            # New email
            email = EmailMessage(
                header,
                message,
                FROM_EMAIL,
                [token.student.AcademicEmail()]
            )

            # Uncomment the line bellow to send emails
            #email.send()
    except:
        raise Http404("Erro ao enviar emails")



    return render(request, 'gda/generate.html')


# This is the function to create the view from the token
def dealToken(request, code, year, semester, classes, token):
    try:
        # First we dicover wich is the discipline
        discipline = Class.objects.all().get(
            code = code.upper(),
            year = year,
            semester = semester,
            class_id = classes
        )
        # Search for token
        token = Token.objects.all().get(
            discipline = discipline,
            token = token,
        )

        print(token)

        out = {
            'discipline': discipline,
            'token': token,
        }
        return render(request, 'gda/vote.html', out)
    except:
        return render(request, 'gda/vote.html')
