from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^disciplines/(?P<institute>[A-Za-z]{2,4})', views.updateDisciplines, name='updateDisciplines'),
]
