from django.shortcuts import render, get_object_or_404
from apps.article.models import Clasificacion, Articulo
from apps.adminview.models import Templates, Available_design_page, enterprisedata, indexDesign, politics
from django.http import HttpResponse
from apps.cart.models import Cart, CartItem

#importaciones para las imagenes
from apps.article.models import Articulo
from PIL import Image

def index(request):
	templates = Templates.objects.get(isSelected=True)
	categoria=Clasificacion.objects.filter(existencia=True)
	blockcat=Clasificacion.objects.filter(existencia=True)[:3]
	articulo=Articulo.objects.filter(existencia=True).exclude(cantidad=0)[:6]
	design=Available_design_page.objects.get(isSelected=True)
	enterprise=enterprisedata.objects.get()
	indexPage=indexDesign.objects.get()

	cart_obj, new_obj = Cart.objects.new_or_get(request)
	items= Articulo.objects.filter(cartitem__id_cart_fk=cart_obj.id)

	contexto={
			  'categoria':categoria,
	 		  'articulo':articulo,
			  'templates':templates,
			  'design':design,
			  'blockcat':blockcat,
			  'indexPage':indexPage,
			  'cart': cart_obj,
			  'items': items,
			  'enterprise':enterprise
			 }
	if design.id==0:
		return render (request, 'home/index.html', contexto)
	if design.id==1:
		return render (request, 'home/index2.html', contexto)
	if design.id==2:
		articulo=Articulo.objects.filter(existencia=True)[:8]
		contexto={
		          'categoria':categoria,
		          'articulo':articulo,
				  'templates':templates,
				  'design':design,
				  'blockcat':blockcat,
				  'indexPage':indexPage,
				  'cart': cart_obj,
				  'items': items,
				  'enterprise':enterprise
				  }
		return render (request, 'home/index3.html', contexto)
	if design.id==3:
		return render (request, 'home/index4.html', contexto)
	return render (request, 'home/index.html', contexto)

def policy(request, option):
	templates = Templates.objects.get(isSelected=True)
	categoria=Clasificacion.objects.filter(existencia=True)
	blockcat=Clasificacion.objects.filter(existencia=True)[:3]
	polic = politics.objects.get(id=0)
	if option == 1:
		policy = True
		cookies = False
		privacy = False
	if option == 2:
		privacy = True
		cookies = False
		policy = False
	if option == 3:
		cookies = True
		privacy = False
		policy = False
	contexto = {'policy':policy,'cookies':cookies,'privacy':privacy,
				'templates':templates,'categoria':categoria,'blockcat':blockcat,
				'polic':polic}
	return render (request, 'policy/policy.html', contexto)

def preload_presentation(request, option):
	
	if option == 1:
		obj = get_object_or_404(indexDesign, pk=0)
		img = Image.open(obj.carrousel1.path)
	if option == 2:
		obj = get_object_or_404(indexDesign, pk=0)
		img = Image.open(obj.carrousel2.path)
	if option == 3:
		obj = get_object_or_404(indexDesign, pk=0)
		img = Image.open(obj.carrousel3.path)
	if option == 4:
		obj = get_object_or_404(indexDesign, pk=0)
		img = Image.open(obj.carrousel4.path)
	if option == 5:
		obj = get_object_or_404(indexDesign, pk=0)
		img = Image.open(obj.portada.path)
	if option == 6:
		obj = get_object_or_404(enterprisedata, pk=0)
		img = Image.open(obj.logo.path)
	response = HttpResponse(content_type='image/%s' % img.format)
	img.save(response, img.format)
	response['Content-Disposition'] = 'filename="image.%s"' % img.format
	return response

def preload_image(request, pk):
	articulo = get_object_or_404(Articulo, pk=pk)
	img = Image.open(articulo.nombre_imagen.path)
	response = HttpResponse(content_type='image/%s' % img.format)
	img.save(response, img.format)
	response['Content-Disposition'] = 'filename="image.%s"' % img.format
	return response