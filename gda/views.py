from django.shortcuts import render
from django.http import Http404
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from gda.tools.tokenGenerator import generateToken
from dacParser.models import Class, Student
from gda.models import Token

URL = 'http://127.0.0.1:8000/'
FROM_EMAIL = 'GDA TESTER <gdatester@gmail.com>'


# Generates tokens for all the students from a discipline
# /manage/d/MM000/YYYY/S/C/generate
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
            tkn_str = generateToken(student.name+discipline.code)
            token, created = Token.objects.all().get_or_create(
                token = tkn_str,
                student = student,
                discipline = discipline
            )
            students_ok.append(token.student)

        out = {
            'discipline': discipline,
            'students': students_ok,
        }
    except:
        raise Http404("Não foi possivel gerar token")

    return render(request, 'gda/generateToken.html', out)


# Send email for all the students in a class
# /manage/d/MM000/YYYY/S/C/send
@login_required
def sendMail(request, code, year, semester, classes):
    try:
        generateTokens(request, code, year, semester, classes)
    except:
        raise Http404("Não foi possivel gerar token")
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
    except:
        raise Http404("Não encontrou a materia desejada")

    try:
        # Now we generate an email for each student in the discipline
        for token in tokens.all():
            header = '[GDA][%s] Avaliação da matéria %s' % (discipline.code,
                                                            discipline)
            link = URL + 'vote' + str(discipline.url()) + '/' + str(token.token)
            message = 'Olá, essa é uma mensagem automatica para envio do link de votação do GDA. \nO link para sua votação é: %s\nO link é a unica maneira de votar, então guarde secretamente o seu link <3\n\n' % link

            # New email
            email = EmailMessage(
                header,
                message,
                FROM_EMAIL,
                [token.student.AcademicEmail()]
            )

            # I wrote these prints just to show whas going on
            print('TO: ' + str(token.student))
            print(header)
            print(message)
            # Uncomment the line bellow to send emails
            #email.send()
    except:
        raise Http404("Erro ao enviar emails")

    out = {
        'discipline': discipline,
    }

    return render(request, 'gda/sendEmail.html', out)


# This is the function to create the view from the token page
# /vote/d/MM000/YYYY/S/C/TOKEN
def dealToken(request, code, year, semester, classes, token):
    try:
        # First we dicover wich is the discipline
        discipline = Class.objects.all().get(
            code = code.upper(),
            year = year,
            semester = semester,
            class_id = classes
        )
        print(discipline)
        # Search for token
        token_obj = Token.objects.all().get(
            discipline = discipline,
            token = token,
        )

        if token_obj:
            out = {
                'discipline': discipline,
                'token': token_obj,
            }
            return render(request, 'gda/vote.html', out)
        else:
            return render(request, 'gda/vote.html')
    except:
        raise Http404("Erro ao procurar tokens")
