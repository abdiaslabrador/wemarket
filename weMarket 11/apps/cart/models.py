from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.myuser.models import CustomUser
from apps.article.models import Articulo
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
# Create your models here.

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
	
	def new_or_get(self, request):
		#pregunta si hay algun carro con esta sesión
		cart_id = request.session.get('cart_id', None)
		#busca al carro
		qs = Cart.objects.filter(id=cart_id)
		#si hay uno entonces no hay que crear un nuevo carro, hay que verificar tiene tiene sesion asignada o no
		if qs.count() == 1:
			#colocamos que no se creo un objeto nuevo carro
			new_obj=False
			cart_obj=qs.first()
			#si está auntenticado y el carro de la sesion no tiene usuario asignado, se le asigna
			if request.user.is_authenticated and cart_obj.id_usuario_fk is None:
				cart_obj.id_usuario_fk=request.user
				cart_obj.save()
		#de otra manera se crea un carro nuevo, y se le asigna el usuario ya sea auntenticado o no	
		else:
			cart_obj=Cart.objects.new(user=request.user) #se crea el carro
			request.session['cart_id']=cart_obj.id #se le asigna la id (es la pk de el carro)
			new_obj=True #fue creado un carro nuevo
		return cart_obj, new_obj

	def new(self, user=None):
		user_obj=None
		if user is not None:
			if user.is_authenticated:
				user_obj=user
		return self.model.objects.create(id_usuario_fk=user_obj)

class Cart(models.Model):

	total = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=0.00)
	subtotal = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=0.00)
	
	update= models.DateTimeField(auto_now=True)
	timestamp= models.DateTimeField(auto_now_add=True)

	#Foreignkeys
	id_usuario_fk=models.ForeignKey(
										User,
	 									null=True, blank=True,
										on_delete=models.CASCADE,
										db_column='id_usuario_fk'
									)
	#items= models.ManyToManyField(CartItem)
	#id_productos_fk=models.ManyToManyField(Articulo)
	objects=CartManager()

	def __str__(self):
		return "id_carro: " + str(self.id)

class CartItem(models.Model):
	quantity	= models.IntegerField(null=True, blank=True, default=1)
	total 		= models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=0.00)	

	update		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	
	
	#Foreignkeys
	id_cart_fk		=models.ForeignKey(
										Cart,
										 on_delete=models.CASCADE,
										 db_column='id_cart_fk',
										 null=True, blank=True
										 )
	id_productos_fk	=models.ForeignKey(
										Articulo,
										on_delete=models.CASCADE,
										db_column='id_productos_fk'
										)

	def __str__(self):
		return str(self.id_cart_fk.id)


def pre_total(sender, instance, *args, **kwargs):	
	instance.total= instance.id_productos_fk.precio * float(instance.quantity)
pre_save.connect(pre_total, sender=CartItem)



def post_total(sender, instance, *args, **kwargs):	
	
	try :
		cart_obj= Cart.objects.get(id=instance.id_cart_fk.id)
		subtotal=0
		total=0
		for x in cart_obj.cartitem_set.all():
			subtotal=Decimal(subtotal) + x.total

		cart_obj.subtotal= Decimal(subtotal)
		cart_obj.total= Decimal(subtotal) + (Decimal(subtotal) * Decimal('0.16'))
		cart_obj.save()
	except Cart.DoesNotExist:
		print("El carro a sido eliminado mente pilas!!")
		pass


post_save.connect(post_total, sender=CartItem)
post_delete.connect(post_total, sender=CartItem)

#post_delete.connect(item_receiver, sender=CartItem)

"""
def pre_save_cart_receiver(sender, instance, *args, **kwargs):
	instance.total= Decimal(instance.subtotal) + (Decimal(instance.subtotal) * Decimal('0.16'))

pre_save.connect(pre_save_cart_receiver, sender=Cart)"""


#instace of cart_obj

"""def m2m_changed_receiver(sender, instance, action,*args, **kwargs):
	if action == "post_add" or action == "post_remove" or action == "post_clear":
		article= instance.id_productos_fk.all()
		total=0
		for x in article:
			total+= Decimal(x.precio)
			
		instance.subtotal=total
		instance.save()

m2m_changed.connect(m2m_changed_receiver, sender=CartItem.id_productos_fk.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
	instance.total= Decimal(instance.subtotal) + (Decimal(instance.subtotal) * Decimal('0.16'))

pre_save.connect(pre_save_cart_receiver, sender=Cart)
"""
