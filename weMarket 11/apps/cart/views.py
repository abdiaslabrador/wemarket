from django.shortcuts import render, redirect, reverse
from apps.adminview.models import Templates
from apps.article.models import Clasificacion, Articulo
from django.conf import settings
from .models import Cart, CartItem
from decimal import Decimal

# Create your views here.

user=settings.AUTH_USER_MODEL


def cart_home(request):
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	#here we're gonna get the cart to use the items to show those in the cart_home
	cart_obj, new_obj= Cart.objects.new_or_get(request)


	#verify if any article already exhausted
	cart_item= cart_obj.cartitem_set.all()
	for item in cart_item:
		if item.quantity > item.id_productos_fk.cantidad or item.id_productos_fk.existencia == False: #if exhausted delete from cart
			remove_from_cart(request, item.id)


	# quantity of cart icon
	request.session['cart_total']= cart_obj.cartitem_set.count()

	if request.session['cart_total']==0:
		empty_cart = True
		empty_message = "El carro no tiene articulos"
	else:
		empty_cart=False
		empty_message = ""

	contexto = {
				  'categoria':categoria,
				  'templates':templates, 
				  'cart': cart_obj,
				  "empty_cart":empty_cart,
				  "empty_message":empty_message,
				}

	return render(request, 'cart/cart.html', contexto)

def remove_from_cart(request, cart_item_id):
	#may be the cart_id doesn't exist, then you need to redirect to another page
	try:
		cart_id=request.session['cart_id']
		cart= Cart.objects.get(id=cart_id)
	except Cart.DoesNotExist:
		print("El carro no existe, o sucede algo")
		return redirect('cart:cart_home')

	#may be the cart_item_id doesn't exist, then you need to redirect to another page
	try:
		cart_item = CartItem.objects.get(id=cart_item_id)
		print("el id de cart_item no existe")
	except CartItem.DoesNotExist:
		return redirect('notfound:notfound')

	cart_item.delete()

	print("Se ha eliminado el carro item exitosamente")
	return redirect('cart:cart_home')

def add_to_cart(request, article_id):
	#estabamos haciendo pruebas con el try y el except, ya no es necesario por que se
	#pasa la variable qty=0 cuando se quiere eliminar un producto,
	#por lo tanto siempre va a tener valores
	qty= request.POST.get('qty', None)

	if qty:
		update_qty=True
	else:
		qty= 0
		update_qty=False


	if article_id is not None:
		try:
			article_object= Articulo.objects.get(id=article_id)
		except article_object.DoesNotExist:
			print("El articulo no fue encontrado")
			return redirect('notfound:notfound')
		
		#this returns the cart
		cart_obj, new_cart= Cart.objects.new_or_get(request)

		#this returns the items of the cart
		cart_item, new_item= CartItem.objects.get_or_create(id_cart_fk= cart_obj, id_productos_fk=article_object)

		#esta condicion de abajo se hizo a manera de prueba, la dejamos por si acaso
		if qty and update_qty:
			if int(qty)==0:
				cart_item.delete()
			else:
				cart_item.quantity=qty
				#cart_item.total= float(qty) * cart_item.id_productos_fk.precio
				cart_item.save()
				
		else:
			print("algo está pasando, revisa la qty")
		"""
		subtotal=0
		for x in cart_obj.cartitem_set.all():
			subtotal+=x.total
		cart_obj.subtotal=subtotal
		cart_obj.total= Decimal(subtotal) + (Decimal(subtotal) * Decimal('0.16'))
		cart_obj.save()
		"""
		#remove an article from the cart
		#if cart_item in cart_obj.items.all():
		#	cart_obj.items.remove(cart_item)
		#add an article to cart
		#else:
		#	cart_obj.items.add(cart_item)
	request.session['cart_total']= cart_obj.cartitem_set.count()

	#this show the article itself
	#return redirect(reverse('article:show_article', args=(article_object.id,)))
	return redirect('cart:cart_home')
	#return redirect('home_app:index')
