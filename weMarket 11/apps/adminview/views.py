from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from apps.article.models import Clasificacion, Articulo
from apps.adminview.forms import (
									ClasificacionForm, ArticleForm, EnterpriseForm,
 									UserForm, ContactForm, IndexForm, MemberForm, 
 									PoliticsForm, admin_givenForm,
 								  )
from apps.adminview.models import Templates, Available_design_page, enterprisedata, teamMembers, contactData, indexDesign, politics
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.myuser.models import CustomUser
from PIL import Image
from django.http import HttpResponse
from apps.factura.models import Factura, Factura_det
from django.db.models import ( Count, Q, Sum)
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def clean_designs():
	templates = Templates.objects.all()
	for templates in templates:
		templates.temp_selected = False
		templates.save()
		temp = Templates.objects.get(isSelected=True)
		temp.temp_selected = True
		temp.save()
	templ = Available_design_page.objects.all()
	for templ in templ:
		templ.temp_selected = False
		templ.save()
		temp2 = Available_design_page.objects.get(isSelected=True)
		temp2.temp_selected = True
		temp2.save()

@login_required
def index_admin(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	total_user = CustomUser.objects.filter().count()
	bought_user = CustomUser.objects.filter(factura__activa=True).values('email').annotate(cant=Count('email')).count()

	#rate_convertion
	rate_covertion= (bought_user*100)/(total_user)
	rate_convertion=int(rate_covertion)

	#buyings of unretire
	buy_unretire=Factura.objects.filter(entregado=False).count()
	
	#profit monthly
	month=timezone.now().month
	year=timezone.now().year
	factura_per_month=Factura.objects.filter(fecha__year=year).filter(fecha__month=month).aggregate(sum=Sum('total'))
	factura_per_month=factura_per_month['sum']
	
	
	#profit yearly
	factura_per_year=Factura.objects.filter(fecha__year=year).aggregate(sum=Sum('total'))
	factura_per_year=factura_per_year['sum']

	#The most values 
	greater_values=Factura_det.objects.filter(id_productos_fk__existencia=True, id_factura_fk__activa=True).values('id_productos_fk__nombre_producto').annotate(appreciation=Sum('valoracion')).filter(appreciation__gt=0).order_by('-appreciation')[0:5]
	print("estos son los artículos por valoracion: \n", greater_values)

	#detail profit yearly
	total_factura_detail=[]
	for i in range(12):
		month_=Factura.objects.filter(fecha__year=year).filter(fecha__month=i+1).aggregate(month=Sum('total'))
		if month_['month'] == None:
			month_=0
			total_factura_detail.insert(i, month_)
		else:
			total_factura_detail.insert(i, int(month_['month']))

	#profit monthly
	total_article_sold_detail=[]
	for i in range(12):
		cantidad=Factura_det.objects.filter(id_factura_fk__activa=True, id_factura_fk__fecha__year=year, id_factura_fk__fecha__month=i+1).aggregate(month=Sum('quantity'))
		if cantidad['month'] == None:
			cantidad=0
			total_article_sold_detail.insert(i, cantidad)
		else:
			total_article_sold_detail.insert(i, cantidad['month'])	

	# sold articles
	sold_articles=0
	for x in total_article_sold_detail:
		sold_articles=x+sold_articles		
	
	#all users (year)
	total_user=CustomUser.objects.filter().count()

	#new registered users (year)
	negative_year=False
	user_this_year=CustomUser.objects.filter( date_joined__year=year).count()
	if user_this_year == 0:
		print("No hay usuarios de este año")

	user_past_year=CustomUser.objects.filter( date_joined__year=year-1).count()
	if user_past_year == 0:
		porcent_user_year = user_this_year*100
		print("No hay usuarios del año pasado")
	else:
		#print("Este anio: ", user_this_year, " \n Anio pasado: ", user_past_year)
		
		porcent_user_year=int((user_this_year * 100)/user_past_year)
		if porcent_user_year < 100:
			porcent_user_year= (100 - porcent_user_year)
			negative_year=True
			

	#new registered users (month)
	negative_month=False
	user_this_month=CustomUser.objects.filter( date_joined__year=year).filter(date_joined__month=month).count()
	if user_this_month == 0:
		print("No hay usuarios de este mes")

	user_past_month=CustomUser.objects.filter( date_joined__year=year).filter(date_joined__month=month-1).count()
	if user_past_month == 0:
		porcent_user_month = user_this_month*100
		print("No hay usuarios del mes pasado")
	else:
		#print("Este mes: ", user_this_month, " \n Mes pasado: ", user_past_month)
		negative_month=False
		porcent_user_month=int((user_this_month * 100)/user_past_month)
		if porcent_user_month < 100:
			porcent_user_month= (100 - porcent_user_month)
			negative_month=True

	#the sellest category
	#total de venta en la categoria
	categories=Clasificacion.objects.filter(existencia=True, articulo__factura_det__id_factura_fk__activa=True).values('nombre_clasificacion').annotate(cant_sell=Count('nombre_clasificacion')).order_by('cant_sell')[0:6]
	if categories == None:
		print("hey no hay categories pendiente")
	else:	
		categories=list(categories)

		#aquí obtengo las categorias más bendidas
		i =0
		for x in categories:
			articles= Articulo.objects.filter(id_clasificacion_fk__nombre_clasificacion__icontains=x['nombre_clasificacion']).filter( factura_det__id_factura_fk__activa=True).values('nombre_producto').annotate(cant_sell=Count('nombre_producto'))
			categories[i]['cant_sell']=len(articles)
			i+=1

		#aquí obtengo los artículos, una ves que obtengo las categorías más bendidas
		total_product=[]
		i=0
		for x in categories:
			total=Articulo.objects.filter(id_clasificacion_fk__existencia=True, id_clasificacion_fk__nombre_clasificacion__icontains=x['nombre_clasificacion']).aggregate(total_producto=Count('existencia'))
			total=total['total_producto']		
			categories[i]['total_producto']=total
			i+=1

		# luego que ya tengo los diccionarios, procedo a anexarle los porcentajes en base  a cada categoría
		for x in categories:
			x['porcent']=int((x['cant_sell']*100)/x['total_producto'])

	

	contexto = {
				'categoria':categoria, #we use this for templates
				'rate_convertion':rate_convertion,
				'buy_unretire':buy_unretire,
				'factura_per_month':factura_per_month,
				'factura_per_year':factura_per_year,
				'greater_values':greater_values,
				'total_factura_detail':total_factura_detail,
				'total_article_sold_detail':total_article_sold_detail,
				'sold_articles':sold_articles,				
				'total_user':total_user,
				'user_this_month':user_this_month,
				'user_past_month':user_past_month,
				'user_this_year':user_this_year,
				'user_past_year':user_past_year,
				'porcent_user_month':porcent_user_month,
				'porcent_user_year':porcent_user_year,
				'negative_year':negative_year,
				'negative_month':negative_month,
				'categories':categories,

				}
	return render(request, 'adminview/index.html', contexto)

def preload_image(request, pk):
	templates = get_object_or_404(Templates, pk=pk)
	img = Image.open(templates.image_path)
	response = HttpResponse(content_type='image/%s' % img.format)
	img.save(response, img.format)
	response['Content-Disposition'] = 'filename="image.%s"' % img.format
	return response

def preload_carrousel(request, pk, option):
	design_page = get_object_or_404(Available_design_page, pk=pk)
	if option == 1:
		img = Image.open(design_page.image_path)
	if option == 2:
		img = Image.open(design_page.image_path1)
	if option == 3:
		img = Image.open(design_page.image_path2)
	response = HttpResponse(content_type='image/%s' % img.format)
	img.save(response, img.format)
	response['Content-Disposition'] = 'filename="image.%s"' % img.format
	return response

@login_required
def article(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	articulo = Articulo.objects.filter(existencia=True).order_by('nombre_producto')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	paginator = Paginator(articulo, 10)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'categoria':categoria,
				'items':items}
	return render(request, 'adminview/article.html', contexto)

@login_required
def choosedesign(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	design = Available_design_page.objects.filter().order_by('type_design')
	contexto = {'design':design}
	return render(request, 'adminview/design_page.html', contexto)

@login_required
def design(request):
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	templates = Templates.objects.filter().order_by('template_name')
	contexto = {'templates':templates}
	return render(request, 'adminview/design.html', contexto)

@login_required
def save_template(request, id_template):
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	tempo  = Templates.objects.get(isSelected=True)
	tempo.isSelected = False
	tempo.temp_selected = False
	tempo.save()
	temp = Templates.objects.get(id=id_template)
	temp.isSelected = True;
	temp.temp_selected = True
	temp.save()
	templates = Templates.objects.filter().order_by('template_name')
	saveChanges = True
	contexto = {'templates':templates,
				'saveChanges':saveChanges}
	return render(request, 'adminview/design.html', contexto)

@login_required
def save_design(request, id_design):
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	tempo  = Available_design_page.objects.get(isSelected=True)
	tempo.isSelected = False
	tempo.temp_selected = False
	tempo.save()
	temp = Available_design_page.objects.get(id=id_design)
	temp.isSelected = True;
	temp.temp_selected = True
	temp.save()
	design = Available_design_page.objects.filter().order_by('name')
	saveChanges = True
	contexto = {'design':design,
				'saveChanges':saveChanges}
	return render(request, 'adminview/design_page.html', contexto)

@login_required
def select_template(request, id_template):
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	temp = Templates.objects.get(temp_selected=True)
	temp.temp_selected=False
	temp.save()
	template = Templates.objects.get(id=id_template)
	template.temp_selected=True
	template.save()
	templates = Templates.objects.filter().order_by('template_name')
	contexto = {'templates':templates}
	return render(request, 'adminview/design.html', contexto)

@login_required
def user_delete(request, id_user, actual_user):
	if request.user.is_staff == False:
		return redirect('home:index')
	users = CustomUser.objects.get(pk=id_user)
	if users.is_active == True and id_user != actual_user:
		users.is_active = False
		users.save()
		return redirect('adminview:users')
	else:
		return redirect('adminview:advice_user')
	
@login_required
def delete_member(request, id_member):
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	memb = teamMembers.objects.get(pk=id_member)
	memb.existencia = False
	memb.save()
	return redirect('adminview:save_page')

@login_required
def save_page(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	saveChanges = True
	contact = contactData.objects.get(id=0)
	temp = Templates.objects.get(temp_selected=True)
	enterprise = enterprisedata.objects.get(id=0)
	polic = politics.objects.get(id=0)
	members = teamMembers.objects.filter(existencia=True)
	design = Available_design_page(isSelected=True)
	indexPage = indexDesign.objects.get()
	if request.method == 'GET':
		form = EnterpriseForm(instance=enterprise)
		form2 = ContactForm(instance=contact)
		form3 = IndexForm(instance=indexPage)
		form4 = IndexForm(instance=polic)
	else:
		form = EnterpriseForm(request.POST or None, request.FILES or None, instance=enterprise)
		form2 = ContactForm(request.POST or None, request.FILES or None, instance=contact)
		form3 = IndexForm(request.POST or None, request.FILES or None, instance=indexPage)
		form4 = PoliticsForm(request.POST or None, request.FILES or None, instance=polic)
		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			form3.save()
			form4.save()
			return redirect('adminview:save_page')
		else:
			diccionario=request.POST
			
		return redirect('adminview:edit_design')
	contexto = {'form':form,
				'form2':form2,
				'form3':form3,
				'form4':form4,
				'members':members,
				'design':design,
				'enterprise':enterprise,
				'contact':contact,
				'polic':polic,
				'indexPage':indexPage,
				'saveChanges':saveChanges,
				}
	return render(request, 'adminview/edit_design.html', contexto)

@login_required
def edit_design(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	saveChanges = True
	contact = contactData.objects.get(id=0)
	temp = Templates.objects.get(temp_selected=True)
	enterprise = enterprisedata.objects.get(id=0)
	polic = politics.objects.get(id=0)
	members = teamMembers.objects.filter(existencia=True)
	design = Available_design_page(isSelected=True)
	indexPage = indexDesign.objects.get()
	if request.method == 'GET':
		form = EnterpriseForm(instance=enterprise)
		form2 = ContactForm(instance=contact)
		form3 = IndexForm(instance=indexPage)
		form4 = IndexForm(instance=polic)
	else:
		form = EnterpriseForm(request.POST or None, request.FILES or None, instance=enterprise)
		form2 = ContactForm(request.POST or None, request.FILES or None, instance=contact)
		form3 = IndexForm(request.POST or None, request.FILES or None, instance=indexPage)
		form4 = PoliticsForm(request.POST or None, request.FILES or None, instance=polic)
		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			form3.save()
			form4.save()
			return redirect('adminview:save_page')
		else:
			diccionario=request.POST
			
		return redirect('adminview:edit_design')
	contexto = {'form':form,
				'form2':form2,
				'form3':form3,
				'form4':form4,
				'members':members,
				'design':design,
				'polic':polic,
				'enterprise':enterprise,
				'contact':contact,
				'indexPage':indexPage,
				}
	return render(request, 'adminview/edit_design.html', contexto)

@login_required
def edit_user(request, id_user, active_user):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')

	if active_user != id_user:
		user = CustomUser.objects.get(id=id_user)
		if request.method == 'POST':
			
			form = UserForm(request.POST, instance=user)
			if form.is_valid():
				form.save()
				user.rol=request.POST['rol']
				user.save()
				if user.rol == "Corriente":
					user.is_staff = False
					user.is_superuser = False
				if user.rol == "Moderador":
					user.is_staff = True
					user.is_superuser = False
				if user.rol == "Administrador":
					user.is_staff = True
					user.is_superuser = True
				return redirect('adminview:users')
			else:
				return render(request, 'adminview/edit_user.html', {'form':form, 'user':user})

		else:

			form = UserForm(instance=user)
			return render(request, 'adminview/edit_user.html', {'form':form, 'user':user})
	else:

		users = CustomUser.objects.filter(is_active=True).order_by('first_name')
		paginator = Paginator(users, 10)
		page = request.GET.get('page')
		error = True
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
		contexto = {'users':users,'error':error}
		return render(request, 'adminview/users.html', contexto)
	
@login_required
def select_design(request, id_design):
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	temp = Available_design_page.objects.get(temp_selected=True)
	temp.temp_selected=False
	temp.save()
	template = Available_design_page.objects.get(id=id_design)
	template.temp_selected=True
	template.save()
	design = Available_design_page.objects.filter().order_by('name')
	contexto = {'design':design}
	return render(request, 'adminview/design_page.html', contexto)

@login_required
def advice_user(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	users = CustomUser.objects.filter(is_active=True).order_by('first_name')
	paginator = Paginator(users, 10)
	page = request.GET.get('page')
	advice = True
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	contexto = {'users':users,'advice':advice}
	return render(request, 'adminview/users.html', contexto)

@login_required
def users(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	users = CustomUser.objects.filter(is_active=True).order_by('first_name')
	paginator = Paginator(users, 10)
	page = request.GET.get('page')
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	contexto = {'users':users,}
	return render(request, 'adminview/users.html', contexto)

@login_required
def sells(request):
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	bills=Factura.objects.filter(activa=True).order_by('-fecha', '-hora')

	contexto = {
				'bills':bills,
			   }
	return render(request, 'adminview/sells.html', contexto)

@login_required
def admin_given(request, id_bill):

	if request.user.is_staff == False:
		return redirect('home:index')
	try:
		bill= Factura.objects.get(id=id_bill)
	except Factura.DoesNotExist:
		print('La factura a sido eliminada previamente o sucedió algo')
		return redirect('notfound:notfound')

	clean_designs()
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	admin_mode=True

	
	if request.method == 'POST':
		form=admin_givenForm(request.POST, instance=bill)
		if form.is_valid():
			
			if form.cleaned_data['entregado']:
				bill.fecha_entregado=timezone.now()
			else:
				bill.fecha_entregado=None
			form.save()
			return redirect('adminview:sells')
	else:
		form=admin_givenForm(instance=bill)	

	contexto = {
				'categoria':categoria,
				'templates':templates,
				'bill':bill,
				'admin_mode':admin_mode,
				'form':form,
			   }
	template= 'adminview/review_bill.html'
	return render(request, template, contexto)

@login_required
def delete_bill(request, id_bill):
	if request.user.is_staff == False:
		return redirect('home:index')
	try:
		bill= Factura.objects.get(id=id_bill)
	except Factura.DoesNotExist:
		print('La factura a sido eliminada previamente o sucedió algo')
		return redirect('notfound:notfound')

	clean_designs()

	if bill.activa == True:
		bill.activa = False
		bill.save()
	return redirect('adminview:sells')

@login_required
def cuadricula(request):
	
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	articulo = Articulo.objects.filter(existencia=True).order_by('nombre_producto')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	paginator = Paginator(articulo, 6)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'categoria':categoria,
				'items':items}
	return render(request, 'adminview/cuadricula.html', contexto)

@login_required
def clasification(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	paginator = Paginator(categoria, 10)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'items':items}
	return render(request, 'adminview/clasification.html', contexto)

@login_required
def delete_article(request, id_article):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	articulo = Articulo.objects.get(id=id_article)
	if articulo.existencia == True:
		articulo.existencia = False
		articulo.save()
	return redirect('adminview:article')

@login_required
def delete_clasificacion(request, id_category):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	clasificacion = Clasificacion.objects.get(id=id_category)
	if clasificacion.existencia == True:
		clasificacion.existencia = False
		clasificacion.save()
		articulo = Articulo.objects.filter(id_clasificacion_fk=id_category).order_by('nombre_producto')
		for articulo in articulo:
			if articulo.existencia == True:
				articulo.existencia = False
				articulo.save()
	return redirect('adminview:clasification')

@login_required
def order_by_list(request, id_category):
	
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	articulo = Articulo.objects.filter(id_clasificacion_fk=id_category).filter(existencia=True)
	paginator = Paginator(articulo, 10)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'categoria':categoria,
				'items':items}
	return render(request, 'adminview/article.html', contexto)

@login_required
def order_by_cuadr(request, id_category):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	articulo = Articulo.objects.filter(id_clasificacion_fk=id_category).filter(existencia=True)
	paginator = Paginator(articulo, 6)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'categoria':categoria,
				'items':items}
	return render(request, 'adminview/cuadricula.html', contexto)

@login_required
def edit_article(request, id_article):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	articulo = Articulo.objects.get(id=id_article)
	if request.method == 'GET':
		form = ArticleForm(instance=articulo)
		form.fields['id_clasificacion_fk'].queryset=Clasificacion.objects.filter(existencia=True)

	else:
		form = ArticleForm(request.POST or None, request.FILES or None, instance=articulo)
		form.fields['id_clasificacion_fk'].queryset=Clasificacion.objects.filter(existencia=True)

		if form.is_valid():
			form.save()
			return redirect('adminview:article')
		else:
			contexto = {
							"form": form,
							'articulo':articulo,
						}
			return render(request, 'adminview/add_article.html', contexto)
	contexto = {
		"form": form,
		'articulo':articulo,
	}
	return render(request, 'adminview/add_article.html', contexto)

@login_required
def edit_clasificacion(request, id_category):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	clasificacion = Clasificacion.objects.get(id=id_category)
	if request.method == 'GET':
		form = ClasificacionForm(instance=clasificacion)
	else:
		form = ClasificacionForm(request.POST, instance=clasificacion)
		if form.is_valid():
			form.save()
		return redirect('adminview:clasification')
	return render(request, 'adminview/edit_clasification.html', {'form':form})

@login_required
def edit_member(request, id_member):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	member = teamMembers.objects.get(id=id_member)
	if request.method == 'GET':
		form = MemberForm(instance=member)
	else:
		form = MemberForm(request.POST or None, request.FILES or None, instance=member)
		if form.is_valid():
			form.save()
			return redirect('adminview:edit_design')
		else:
			diccionario=request.POST
			print('es invalido: ', diccionario)
		return redirect('adminview:edit_design')
	contexto = {
		"form": form,
		'member':member,
	}
	return render(request, 'adminview/add_member.html', contexto)

@login_required
def add_member(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	member = teamMembers.objects.filter(existencia=True)
	form = MemberForm(request.POST or None, request.FILES or None)
	isNew = True
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return redirect('adminview:edit_design')
	contexto = {
		"form": form,
		'isNew': isNew,
		'member':member,
	}
	return render(request, 'adminview/add_member.html', contexto)

@login_required
def searchUser(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.user.is_superuser == False:
		return redirect('adminview:log_required')
	busqueda = request.GET.get('busqueda', '')
	users = CustomUser.objects.filter(email__icontains = busqueda)
	isSearch = True
	paginator = Paginator(users, 10)
	template = 'adminview/users.html'
	page = request.GET.get('page')
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	contexto = {
		'meta_description':'',
		'meta_keywords':'',
		'users':users,
		'isSearch':isSearch
	}
	return render(request, template, contexto)

@login_required
def searchBar(request, option):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	busqueda = request.GET.get('busqueda', '')
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	isSearch = True
	articulo = Articulo.objects.filter(nombre_producto__icontains = busqueda).filter(existencia=True).order_by('nombre_producto')
	if option == '1':
		paginator = Paginator(articulo, 10)
		template = 'adminview/article.html'
	else:
		paginator = Paginator(articulo, 6)
		template = 'adminview/cuadricula.html'
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {
		'meta_description':'',
		'meta_keywords':'',
		'categoria':categoria,
		'items':items,
		'isSearch':isSearch
	}
	return render(request, template, contexto)

@login_required
def searchClasif(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	busqueda = request.GET.get('busqueda', '')
	categoria = Clasificacion.objects.filter(nombre_clasificacion__icontains = busqueda).filter(existencia=True).order_by('nombre_clasificacion')
	paginator = Paginator(categoria, 10)
	page = request.GET.get('page')
	isSearch = True
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'items':items,
				'isSearch':isSearch}
	return render(request, 'adminview/clasification.html', contexto)

@login_required
def add_article(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	articulo = Articulo.objects.filter(existencia=True).order_by('nombre_producto')
	form = ArticleForm(request.POST or None, request.FILES or None)
	form.fields['id_clasificacion_fk'].queryset=Clasificacion.objects.filter(existencia=True)
	isNew = True
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return redirect('adminview:article')
	contexto = {
		"form": form,
		'isNew': isNew,
		'articulo':articulo,
	}
	return render(request, 'adminview/add_article.html', contexto)

@login_required
def add_clasification(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	if request.method == 'POST':
		form = ClasificacionForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('adminview:clasification')
	else:
		form = ClasificacionForm()
	return render(request, 'adminview/edit_clasification.html', {'form':form})

@login_required
def without_stock(request):
	
	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	withoutStock = True
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	articulo = Articulo.objects.filter(Q(cantidad=0) | Q(agotado=True)).filter(existencia=True)
	paginator = Paginator(articulo, 10)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'categoria':categoria,
				'items':items,
				'withoutStock':withoutStock}
	return render(request, 'adminview/article.html', contexto)

def log_required(request):
	if request.user.is_staff == False:
		return redirect('home:index')
	return render(request, 'adminview/login_required.html')

@login_required
def without_stock_cuadricula(request):

	clean_designs()
	if request.user.is_staff == False:
		return redirect('home:index')
	withoutStock = True
	categoria = Clasificacion.objects.filter(existencia=True).order_by('nombre_clasificacion')
	articulo = Articulo.objects.filter(Q(cantidad=0) | Q(agotado=True)).filter(existencia=True)
	paginator = Paginator(articulo, 6)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	contexto = {'meta_description':'',
				'meta_keywords':'',
				'categoria':categoria,
				'items':items,
				'withoutStock':withoutStock}
	return render(request, 'adminview/cuadricula.html', contexto)
