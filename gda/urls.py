from django.conf.urls import url,include
from . import views


urlpatterns = [
    # This is the url to deal with the token
    url(
        r'^(?P<code>[A-Za-z][A-Za-z ][0-9]{3})\/(?P<year>\d{4})\/(?P<semester>\d)\/(?P<classes>[A-Za-z])\/(?P<token>[\w\s\-]+)\/?',
        views.dealToken,
        name='vote'
    ),
]
#
