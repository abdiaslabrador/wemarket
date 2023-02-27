from django.shortcuts import render, redirect
from apps.adminview.models import Templates
from apps.article.models import Clasificacion, Articulo
from apps.cart.models import Cart, CartItem
from apps.article.models import Comment

def delete_comment(request, id_article, id_comment):

	advice = True
	com = Comment.objects.get(pk=id_comment)
	com.existencia = False
	com.save()
	templates = Templates.objects.get(isSelected=True)
	articulo = Articulo.objects.get(id=id_article)
	categoria = Clasificacion.objects.filter(existencia=True)
	comments = Comment.objects.filter(existencia=True, id_article_fk=id_article)
	related = Articulo.objects.filter(id_clasificacion_fk=articulo.id_clasificacion_fk, existencia=True).exclude(id=id_article)[:3]
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	item= CartItem.objects.filter(id_productos_fk=id_article)
	content = request.POST.get('contenido', '')
	subject = request.POST.get('asunto', '')
	if request.method == 'POST':
		b = Comment(contenido=content, asunto=subject, id_article_fk=articulo, id_user_fk=request.user)
		b.save()
	contexto = {
		'advice':advice,
		'categoria':categoria,
		'articulo':articulo,
		'templates':templates,
		'cart': cart_obj,
		'item': item,
		'related':related,
		'comments':comments,
		}

	if articulo.existencia == True:
		return render(request, 'article/article.html', contexto)
	else:
		return redirect('notfound:notfound')

def show_article(request, id_article):
	templates = Templates.objects.get(isSelected=True)
	articulo = Articulo.objects.get(id=id_article)
	categoria = Clasificacion.objects.filter(existencia=True)
	comments = Comment.objects.filter(existencia=True, id_article_fk=id_article)
	related = Articulo.objects.filter(id_clasificacion_fk=articulo.id_clasificacion_fk, existencia=True).exclude(id=id_article)[:3]
	

	
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	try:
		item= CartItem.objects.get(id_cart_fk=cart_obj, id_productos_fk=id_article)
	except:
		item = None
		print(item, " ", id_article)

	content = request.POST.get('contenido', '')
	if request.method == 'POST':
		b = Comment(contenido=content, id_article_fk=articulo, id_user_fk=request.user)
		b.save()

	contexto = {
		'categoria':categoria,
		'articulo':articulo,
		'templates':templates,
		'cart': cart_obj,
		'item': item,
		'related':related,
		'comments':comments,
		}

	if articulo.existencia == True:
		return render(request, 'article/article.html', contexto)
	else:
		return redirect('notfound:notfound')
