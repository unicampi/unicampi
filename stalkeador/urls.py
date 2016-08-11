from django.conf.urls import url, include
from . import views

urlpatterns = [
    # URL for student
    url(
        r'^s/(?P<studentRA>\d{5,6})$',
        views.student,
        name='student'
    ),
    # URL for degrees of discipline
    url(
        # This is a confusing regex it's working but anyhelp would be good
        # d/(?P<code>[A-Za-z][A-Za-z ][0-9]{3}) - This matches the code
        # \/?(?P<year>\d{4})?                   - Optional year
        # \/?(?P<semester>\d)?                  - Optional semester
        # \/?(?P<classes>[A-Za-z])?\/?          - Optional classes
        r'^d/(?P<code>[A-Za-z][A-Za-z ][0-9]{3})\/?(?P<year>\d{4})?\/?(?P<semester>\d)?\/?(?P<classes>[A-Za-z])?\/?',
        views.discipline,
        name='discipline'
    ),
    # URL for index
    url(
        r'^$',
        views.index,
        name='index'
    ),
]
