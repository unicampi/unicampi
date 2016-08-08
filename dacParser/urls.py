from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^disciplines', views.updateDisciplines, name='updateDisciplines'),
]
