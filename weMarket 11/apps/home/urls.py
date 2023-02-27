from django.urls import path
from apps.home.views import index, preload_image, preload_presentation, policy

app_name = 'home_app'

urlpatterns = [
    path('', index, name='index'),
    path('preload/<int:pk>/', preload_image, name='preload_image'),  #esto muestra solo la imagen
    path('presentpreload/<int:option>/', preload_presentation, name='preload_presentation'),  #esto muestra solo la imagen
    path('policy/<int:option>/', policy, name='policy'),  #esto muestra solo la imagen
]