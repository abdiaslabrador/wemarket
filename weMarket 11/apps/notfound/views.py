from django.shortcuts import render
from apps.adminview.models import Templates
from apps.article.models import Clasificacion

# Create your views here.


def notfound(request):
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.all()
	contexto = {'categoria':categoria,'templates':templates}
	return render(request, 'notfound/404.html', contexto)