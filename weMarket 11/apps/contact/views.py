from django.shortcuts import render, get_object_or_404
from apps.adminview.models import Templates, teamMembers, contactData, enterprisedata
from apps.article.models import Clasificacion
from apps.myuser.models import CustomUser

from django.http import HttpResponse
#importaciones para las imagenes
from PIL import Image
# Create your views here.

def preload_image(request, pk, option):
	if option==1:
		opt = get_object_or_404(teamMembers, pk=pk)
		img = Image.open(opt.image_path.path)
	if option==2:
		opt = get_object_or_404(contactData, pk=pk)
		img = Image.open(opt.image_path.path)
	if option==3:
		opt = get_object_or_404(CustomUser, pk=pk)
		img = Image.open(opt.photo.path)
	if option==4:
		opt = get_object_or_404(enterprisedata, pk=pk)
		img = Image.open(opt.logo.path)
	response = HttpResponse(content_type='image/%s' % img.format)
	img.save(response, img.format)
	response['Content-Disposition'] = 'filename="image.%s"' % img.format
	return response

def contact(request):

	contactdata = contactData.objects.get()
	members = teamMembers.objects.filter(existencia=True)
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	enterprise = enterprisedata.objects.get()
	content = request.POST.get('contenido', '')
	name = request.POST.get('nombre', '')
	email = request.POST.get('email', '')
	subject = request.POST.get('asunto', '')
	if request.method == 'POST' and email and name:
		send_mail(subject, content, email, ['kike1996@hotmail.com'], fail_silently=False)
	contexto = {'categoria':categoria,'templates':templates,'members':members,
				'contactdata':contactdata,'enterprise':enterprise}
	return render(request, 'contact/contact.html', contexto)