from apps.adminview.models import Templates
from django.shortcuts import render, redirect
from apps.article.models import Clasificacion, Articulo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index_by_category(request, id_category):
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	articulo = Articulo.objects.filter(existencia=True).filter(id_clasificacion_fk=id_category).order_by('nombre_producto')
	paginator = Paginator(articulo, 9)
	page = request.GET.get('page')
	categoria1 = Clasificacion.objects.get(id=id_category)
	title = categoria1.nombre_clasificacion
	try:
		articulo = paginator.page(page)
	except PageNotAnInteger:
		articulo = paginator.page(1)
	except EmptyPage:
		articulo = paginator.page(paginator.num_pages)
	contexto = {
		'categoria':categoria,
		'articulo':articulo,
		'title':title,
		'templates':templates
		}
	return render(request, 'search/index.html', contexto)

def index(request):
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	articulo = Articulo.objects.filter(existencia=True).order_by('nombre_producto')
	paginator = Paginator(articulo, 9)
	page = request.GET.get('page')
	try:
		articulo = paginator.page(page)
	except PageNotAnInteger:
		articulo = paginator.page(1)
	except EmptyPage:
		articulo = paginator.page(paginator.num_pages)
	contexto = {
		'categoria':categoria,
		'articulo':articulo,
		'templates':templates
		}
	return render(request, 'search/index.html', contexto)

def searchProduct(request):
	categoria = Clasificacion.objects.filter(existencia=True)
	templates = Templates.objects.get(isSelected=True)
	template = 'search/index.html'

	title = request.POST.get('busqueda', '')
	isSearch = True
	if title == '':
		
		return redirect('home:index')
	else:
		articulo = Articulo.objects.filter(nombre_producto__icontains = title).filter(existencia=True).order_by('nombre_producto')
		paginator = Paginator(articulo, 9)
		
		page = request.GET.get('page')
		try:
			articulo = paginator.page(page)
		except PageNotAnInteger:
			articulo = paginator.page(1)
		except EmptyPage:
			articulo = paginator.page(paginator.num_pages)

		
		contexto = {
					'meta_description':'',
					'meta_keywords':'',
					'categoria':categoria,
					'articulo':articulo,
					'title':title,
					'isSearch':isSearch,
					'templates':templates
					}
		return render(request, template, contexto)