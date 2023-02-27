from django.conf.urls import url, include

from apps.notfound.views import notfound

app_name = 'notfound'

urlpatterns = [
    
	url(r'^$', notfound, name="notfound"),
]