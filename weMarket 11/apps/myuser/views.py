from .models import CustomUser
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import RegisterForm, LoginForm, UserConfigurationForm
from django.views.generic import CreateView
from django.contrib.auth import login, update_session_auth_hash
from apps.article.models import Clasificacion
from apps.adminview.models import Templates
from django.contrib.auth.forms import PasswordChangeForm
from apps.factura.models import Factura, Factura_det
from django.contrib.auth.decorators import login_required

	
class RegisterUser(CreateView):
	model= settings.AUTH_USER_MODEL
	form_class = RegisterForm
	template_name = "register/register.html"
	success_url = reverse_lazy('login')

	def get_context_data(self, **kwargs):
		kwargs['templates'] = Templates.objects.get(isSelected=True)
		return super().get_context_data(**kwargs)
	
def LoginView(request):
	templates = Templates.objects.get(isSelected=True)
	# if this is a POST request we need to process the form data
	if request.method == 'POST':

		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)

		# check whether it's valid:
		if form.is_valid():

			# process the data in form.cleaned_data as required
			# redirect to a new URL:
			email=form.cleaned_data.get('email')
			user=CustomUser.objects.get(email=email)
			login(request, user)
			return redirect('home_app:index')
			

	# if a GET (or any other method) we'll create a blank form
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form, 'templates':templates})

@login_required
def index_myuser(request):

	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	contexto = {'categoria':categoria,'templates':templates}
	return render(request, 'myuser/myuser.html', contexto)

@login_required
def history(request):

	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	#return all bills
	bills=Factura.objects.filter(id_usuario_fk=request.user, activa=True).order_by('-fecha', '-hora')

	contexto = {
				'categoria':categoria,
				'templates':templates,
				'bills':bills,
				}
	return render(request, 'myuser/history.html', contexto)

@login_required
def configuration(request):

	categoria = Clasificacion.objects.filter(existencia=True)
	templates = Templates.objects.get(isSelected=True)
	if request.method == 'GET':
		form = UserConfigurationForm(instance=request.user)
	else:
		form = UserConfigurationForm(request.POST or None, request.FILES or None, instance=request.user)
		if form.is_valid():
			form.save()
		return redirect('myuser:myuser')
	return render(request, 'myuser/configuration.html', {'form': form, 'categoria':categoria,'templates':templates})

def reset_password(request):
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user) #don't permit log out
			return redirect('myuser:myuser')
		else:
			return redirect('myuser:reset_password')
	else:
		form = PasswordChangeForm(request.user)
		return render(request, 'myuser/password_reset.html', {'form': form, 'categoria':categoria, 'templates':templates})