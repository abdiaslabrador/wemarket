from django.shortcuts import render, redirect
from .models import Factura, Factura_det
from .forms import User_credit_cardForm, valoracionForm
from apps.cart.models import Cart, CartItem
from apps.adminview.models import Templates
from apps.article.models import Clasificacion
from .utils import code_created
from django.contrib.auth.decorators import login_required
from django.db.models import Avg


@login_required
def Credit_card(request):
	#templates
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	#the cart have to exist
	try:
		cart_id=request.session['cart_id']
		cart_obj= Cart.objects.get(id=cart_id)
	except Cart.DoesNotExist:
		print("El carro no existe, o sucede algo")
		return redirect('cart:cart_home')
	except KeyError:
		print("El cart_id no existe porque fue eliminado previamente")
		return redirect('cart:cart_home')

		#if we have articles into de card
	if request.session.get('cart_total' or None) and request.session.get('cart_total' or None) > 0:
		#the process
		if request.method == 'POST':
			form   = User_credit_cardForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('billing:checkout')
		else:
			form = User_credit_cardForm()

		context= {	
					'categoria':categoria,
					'templates':templates,
					'cart':cart_obj,
					'form':form,
				 }
		template="Checkout/credit_card.html"
		return render(request, template, context)
	else:
		return redirect('cart:cart_home')

@login_required
def Checkout(request):
	try:
		cart_id=request.session['cart_id']
		cart_obj= Cart.objects.get(id=cart_id)
	except Cart.DoesNotExist:
		print("El carro no existe, o sucede algo")
		return redirect('cart:cart_home')
	except KeyError:
		print("El cart_id no existe porque fue eliminado previamente")
		return redirect('cart:cart_home')

	if cart_obj.cartitem_set.count() == 0:
		return redirect('cart:cart_home')


	#the process
	if request.user.money >=cart_obj.total:
		#verify if the quatities of articles changed, whether true we delele the cart
		for item in cart_obj.cartitem_set.all():
			if item.quantity > item.id_productos_fk.cantidad:
				cart_obj.delete()
				del request.session['cart_id']	
				request.session['cart_total']=0
				return redirect('billing:change_qty')
				
					
	#if all are ok, go to buy!
		#here we create a bill
		factura=Factura.objects.create(id_usuario_fk=request.user)
		factura.id_codigo_retiro=code_created(factura)
		factura.subtotal=cart_obj.subtotal
		factura.total=cart_obj.total
		factura.save()

		#assign the bills related
		for item in cart_obj.cartitem_set.all():
			factura_det=Factura_det.objects.create(id_factura_fk=factura)
			factura_det.id_productos_fk= item.id_productos_fk
			factura_det.price_sold=item.id_productos_fk.precio
			factura_det.quantity=item.quantity
			factura_det.total=item.total
			factura_det.save()
			item.id_productos_fk.cantidad-=item.quantity
			if item.id_productos_fk.cantidad == 0:
				item.id_productos_fk.agotado=True
			item.id_productos_fk.save()

		#at last delete the cart
		cart_obj.delete()
		del request.session['cart_id']	
		request.session['cart_total']=0
		

		return redirect('billing:success_checkout')
	else:
		#the person doesn't have enought money
		return redirect('billing:not_money')

@login_required
def Change_qty(request):
	#templates
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	error_quantity=True
	error_quantity_message="La cantidad de articulos a comprar era mayor que la disponible tienes que volver a hacer el carro"

	context= {	
	'categoria':categoria,
	'templates':templates,
	'error_quantity':error_quantity,
	'error_quantity_message':error_quantity_message,
 	}

	template="warning_same_use/same_use.html"
	return render(request, template, context)

@login_required
def Success(request):
	#templates

	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	
	#datas
	bill= Factura.objects.filter(id_usuario_fk=request.user)
	bill1= Factura.objects.latest('fecha', 'hora')
	count= bill.count()
	entre = ""
	if bill1.entregado:
		entre = "Ya fue entregado"
	else:
		entre = "Sin entregar"
	qr_text = "Código de factura: #" + bill1.id_codigo_retiro + "\n" + "Fecha: " + str(bill1.fecha) + "\n" + "Hora: " + str(bill1.hora) + "\n" + "Subtotal: " + str(bill1.subtotal) + " bsS\n" + "Total: " + str(bill1.total) + " bsS\n"  + "Estado: "+ entre + "\n" + "\n" + "Código QR validado por weMarket."

	if count > 0:
		empty_bill = True
		empty_message = "¡Transacción APROBADA!"
		bill= Factura.objects.latest('fecha', 'hora')

	else:
		empty_bill=False
		empty_message = "Aun no posee alguna factura"
		bill=None

	context= {	
				'categoria':categoria,
				'templates':templates,
				'empty_bill':empty_bill,
				'empty_message':empty_message,
				'bill':bill,'qr_text':qr_text,
			 }
	template="Checkout/success_checkout.html"
	return render(request, template, context)
	
@login_required
def Not_money(request):
	#templates
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	not_money=True
	not_money_message = "¡Transacción FALLIDA no posee saldo suficiente!"

	context= {	
				'categoria':categoria,
				'templates':templates,
				'not_money':not_money,
				'not_money_message':not_money_message,
			 }
	template="warning_same_use/same_use.html"
	return render(request, template, context)

@login_required
def Review_bill(request, id_bill):
	#templates
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)
	
	#return the bill that we want to see
	try:
		bill= Factura.objects.get(id=id_bill)
		entre = ""
		if bill.entregado:
			entre = "Ya fue entregado"
		else:
			entre = "Sin entregar"
		qr_text = "Código de factura: #" + bill.id_codigo_retiro + "\n" + "Fecha: " + str(bill.fecha) + "\n" + "Hora: " + str(bill.hora) + "\n" + "Subtotal: " + str(bill.subtotal) + " bsS\n" + "Total: " + str(bill.total) + " bsS\n"  + "Estado: "+ entre + "\n" + "\n" + "Código QR validado por weMarket."
	except Factura.DoesNotExist:
		print('La factura a sido eliminada previamente o sucedió algo')
		return redirect('notfound:notfound')


	context= {	
				'categoria':categoria,
				'templates':templates,
				'bill':bill,
				'qr_text':qr_text
			 }

	template="Checkout/review_bill.html"
	return render(request, template, context)

@login_required
def Bill_value(request, id_bill):
	#templates
	templates = Templates.objects.get(isSelected=True)
	categoria = Clasificacion.objects.filter(existencia=True)

	form = valoracionForm(request.POST)

	#return the bill that we want to value
	try:
		bill= Factura.objects.get(id=id_bill)
	except Factura.DoesNotExist:
		print('La factura a sido eliminada previamente o sucedió algo')
		return redirect('notfound:notfound')

	#if the bill has already been valued
	if bill.valorado:
		already_valued=True
		already_valued_message="¡Esta factura YA ha sido valorada!"
		context= {	
				'categoria':categoria,
				'templates':templates,
				'already_valued':already_valued,
				'already_valued_message':already_valued_message,
			 }
		template="warning_same_use/same_use.html"
		return render(request, template, context)	

	else:
		if bill.entregado: #if the bill has already been delivered, we can value

			if request.method == 'POST':
				
				if form.is_valid():
					#este form es para comprobar que en todas las casillas los datos son correctos
					for item in bill.factura_det_set.all():
						name_product=item.id_productos_fk.nombre_producto
						
						try:#i ensure that the data if type int
							int(request.POST[name_product]) 
						except ValueError: #otherwise  we throw a warning
							bad_data=True
							bad_data_message="¡Introduce datos correctos!"
							context= {	
										'categoria':categoria,
										'templates':templates,
										'bill':bill,
										'bad_data':bad_data,
										'bad_data_message':bad_data_message,
							 		 }
							template="Checkout/bill_value.html"
							return render(request, template, context)

					#if all is ok we got a average and assign it an the value too...
					for item in bill.factura_det_set.all():
						name_product=item.id_productos_fk.nombre_producto
						item.valoracion= request.POST[name_product]
						item.save()
						avg=Factura_det.objects.filter(id_productos_fk=item.id_productos_fk.id).aggregate(avg=Avg('valoracion'))
						avg=avg['avg']
						item.id_productos_fk.valoracion=int(avg)
						item.id_productos_fk.save()
						
					bill.valorado=True
					bill.save()
					return redirect('myuser:history')
				else:
					form = valoracionForm() #really we can delete this line but it doesn't matter
			else:
				context= {	
							'categoria':categoria,
							'templates':templates,
							'bill':bill,
							'form':form,
				 		 }
				template="Checkout/bill_value.html"
				return render(request, template, context)
		else:
			already_given=True
			already_given_message="¡Esta factura No ha sido entregada!"
			context= {	
						'categoria':categoria,
						'templates':templates,
						'already_given':already_given,
						'already_given_message':already_given_message,
			 		}
			template="warning_same_use/same_use.html"
			return render(request, template, context)