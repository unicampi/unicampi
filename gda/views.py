from django.shortcuts import render
from dacParser.models import Class
from gda.models import Token


# Create your views here.
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
