from django.conf.urls import url, include
from django.urls import path
from apps.contact.views import contact, preload_image

app_name = 'contact'

urlpatterns = [

    url(r'^$', contact, name="contact"),
    path('preload/<int:pk>/<int:option>/', preload_image, name='preload_image'),  #esto muestra solo la imagen


]