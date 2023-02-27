"""weMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""    
#Abdías Labrador                Actualizaciones
#correción de error de la base de datos

from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from apps.myuser.views import RegisterUser, LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('apps.home.urls', namespace='home')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('myuser/', include('apps.myuser.urls', namespace='myuser')),
    path('billing/', include('apps.factura.urls', namespace='billing')),
    path('search/', include('apps.search.urls', namespace='search')),
    path('article/', include('apps.article.urls', namespace='article')),
    path('contact/', include('apps.contact.urls', namespace='contact')),
    path('notfound/', include('apps.notfound.urls', namespace='notfound')),
    path('adminview/', include('apps.adminview.urls', namespace='adminview')),
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginView, name="login"),
    path('Logout', views.LogoutView.as_view(template_name='login.html',), name= 'log_out'),
    path('password_reset/', views.PasswordResetView.as_view(template_name='register/password_reset_form.html', email_template_name='register/password_reset_email.html'), name= 'password_reset'),
    path('password_reset/done', views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'), name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm.html'), name= 'password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'), name= 'password_reset_complete'),
]   
    