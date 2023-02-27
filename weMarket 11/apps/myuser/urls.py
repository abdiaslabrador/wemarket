from django.urls import path, include
from apps.myuser import views

#me metí con esto

app_name = 'myuser'
# you've not imported viw from you module
urlpatterns = [
    path('', views.index_myuser, name='myuser'),
    path('history', views.history, name='history'),
    path('configuration', views.configuration, name='configuration'),
    path('reset_password', views.reset_password, name='reset_password'),
]