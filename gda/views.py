from django.shortcuts import render
from django.http import Http404
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.db import transaction

from dacParser.models import Offering, Student, Subject
from gda.models import Choice, Answer, Question
from stalkeador.models import Token

from gda.tools.tokenGenerator import generateToken


URL = 'http://127.0.0.1:8000/'
FROM_EMAIL = 'GDA TESTER <gdatester@gmail.com>'

# This is the function to create the view from the token page
# /vote/d/MM000/YYYY/S/C/TOKEN
@csrf_protect
@transaction.atomic
def dealToken(request, code, year, semester, offerings, token):
    # Searchs the information of the url
    try:
        SubjectQuery = Subject.objects.all().get(
            code = code.upper()
        )
        # First we dicover wich is the discipline
        OfferingQuery = Offering.objects.all().get(
            subject = SubjectQuery,
            year = year,
            semester = semester,
            offering_id = offerings
        )
        # Search for token in that offering
        TokenQuery = Token.objects.all().get(
            offering = OfferingQuery,
            token = token,
        )
    except:
        raise Http404("Não foi possível encontrar o token")

    if TokenQuery.used:
        return render(request, 'gda/questionnaire.html',{'token': TokenQuery})

    # If this was a submission form, we need to check its accuracy
    if request.method == "POST":
        try:
            # Update de database
            with transaction.atomic():
                # Runs through all the questions id
                for question in SubjectQuery.questionnaire.questions.all():
                    if str(question.id) not in request.POST:
                        raise ValueError('Not all questions were in POST')
                    else:
                        value = request.POST[str(question.id)]
                        # Now we should make the security check for the inftion
                        if question.type == 'T':
                            # turns the text into a safe text for html
                            value = mark_safe(value.strip())
                            answer = Answer.objects.create(text=value,
                                                            question=question
                                                            )
                        elif question.type == 'N':
                            # Checks if the answer is a number
                            if value.isdigit():
                                value = value
                                answer = Answer.objects.create(text=value,
                                                            question=question
                                                            )
                            else:
                                raise ValueError('Not valid in Number')
                        elif question.type == 'O':
                            # Check if its a valid choice
                            choiceQuery = Choice.objects.all().get(
                                                                id = int(value)
                                                                )
                            # Checks if this question has this choice
                            if choiceQuery:
                                if choiceQuery in question.choices.all():
                                    answer = Answer.objects.create(text="value",
                                                            choice=choiceQuery,
                                                            question=question
                                                                    )
                                else:
                                    raise ValueError('Not valid in Options')
                    # Save the answer
                    answer.save()
                # After looping through all the questions, we mark token used
                TokenQuery.used = True
                TokenQuery.save()
            return render(request, 'gda/questionnaire.html',{'token': TokenQuery})
        except:
            raise Http404("Parametros das respostas errados")


    if TokenQuery:
        out = {
            'offering': OfferingQuery,
            'token': TokenQuery,
            'questions': SubjectQuery.questionnaire.questions.all(),
        }

        return render(request, 'gda/questionnaire.html', out)
    else:
        return render(request, 'gda/questionnaire.html')


# Generates tokens for all the students from a discipline
# /manage/d/MM000/YYYY/S/C/generate
@login_required
def generateTokens(request, code, year, semester, offerings):
    SubjectQuery = Subject.objects.all().get(
        code = code.upper()
    )
    try:
        # First, gets detials about discipline
        OfferingQuery = Offering.objects.all().get(
            subject = SubjectQuery,
            year = year,
            semester = semester,
            offering_id = offerings
        )
    except Offering.DoesNotExist:
        raise Http404("Não encontrou a materia desejada")

    # Generate a token per student
    #try:
    students_ok = []
    for student in OfferingQuery.students.all():
        token, created = Token.objects.all().get_or_create(
            student = student,
            offering = OfferingQuery
            )
        students_ok.append(token.student)

    out = {
        'discipline': OfferingQuery,
        'students': students_ok,
    }
#    except:
#        raise Http404("Não foi possivel gerar token")

    return render(request, 'gda/generateToken.html', out)


# Send email for all the students in a class
# /manage/d/MM000/YYYY/S/C/send
@login_required
def sendMail(request, code, year, semester, offerings):
    try:
        generateTokens(request, code, year, semester, offerings)
    except:
        raise Http404("Não foi possivel gerar token")

    SubjectQuery = Subject.objects.all().get(
        code = code.upper()
    )
    try:
        # First, gets detials about discipline
        OfferingQuery = Offering.objects.all().get(
            subject = SubjectQuery,
            year = year,
            semester = semester,
            offering_id = offerings
        )
    except Offering.DoesNotExist:
        raise Http404("Não encontrou a materia desejada")

    # Find's all the tokens that is from this class
    try:
        tokens = Token.objects.all().filter(
            offering = OfferingQuery
        )
    except:
        raise Http404("Não encontrou a materia desejada")

    try:
        # Now we generate an email for each student in the discipline
        for token in tokens.all():
            header = '[GDA][%s] Avaliação da matéria %s' % (OfferingQuery.subject.code,
                                                            OfferingQuery)
            link = URL + 'vote' + str(OfferingQuery.url()) + '/' + str(token.token)
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
        'discipline': OfferingQuery,
    }

    return render(request, 'gda/sendEmail.html', out)
