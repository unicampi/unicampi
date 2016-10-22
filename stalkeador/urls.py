from django.conf.urls import url, include
from . import views

urlpatterns = [
    # URL for student
    url(
        r'^s/(?P<studentRA>\d{5,6})$',
        views.deal_student,
        name='student'
    ),
    #url for teachers, need to be improved
    url(r'^t/(?P<teacherID>.*)',
        views.deal_teacher,
        name='teacher'
    ),
    # URL for degrees of discipline
    url(
        # This is a confusing regex it's working but anyhelp would be good
        # d/(?P<code>[A-Za-z][A-Za-z ][0-9]{3}) - This matches the code
        # \/?(?P<year>\d{4})?                   - Optional year
        # \/?(?P<semester>\d)?                  - Optional semester
        # \/?(?P<offe_id>[A-Za-z])?\/?          - Optional offe_id
        r'^d/(?P<code>[A-Za-z][A-Za-z ][0-9]{3})\/?(?P<year>\d{4})?\/?(?P<semester>\d)?\/?(?P<offe_id>[A-Za-z])?\/?',
        views.deal_subject,
        name='subject'
    ),
    # URL for index
    url(
        r'^$',
        views.index,
        name='index'
    ),
]
