from django.db import models
from django.conf import settings
# Create your models here.
from apps.myuser.models import CustomUser
from apps.article.models import Articulo

from .utils import code_created


class Factura(models.Model):
	activa 		= models.BooleanField(default=True) # if we want to delete after
	entregado 	= models.BooleanField(default=False) # if it was delivered
	valorado	= models.BooleanField(default=False)
	fecha 		= models.DateField(auto_now=False,auto_now_add=True)
	hora 		= models.TimeField(auto_now=False, auto_now_add=True)
	
	fecha_entregado = models.DateTimeField(null=True, blank=True)

	total 		= models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=0.00)
	subtotal = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=0.00)
	
	#datos para qr y demas
	id_codigo_retiro = models.CharField(max_length=120, unique=True, null=True, blank=True)	#editable=False
	qr 			= models.TextField(null=True, blank=True)

	#foreignKeys
	id_usuario_fk = models.ForeignKey(
									settings.AUTH_USER_MODEL, 
									on_delete=models.CASCADE, 
									db_column='id_usuario_fk'
									)

	def __str__(self):
		return "N* factura: " + str(self.id) + "  /  N* orden: " + str(self.id_codigo_retiro)

	#here we generate a particular code
	def save(self, *args, **kwargs):
		if self.id_codigo_retiro == None or self.id_codigo_retiro == '':
			self.id_codigo_retiro = code_created(self)
		super(Factura, self).save(*args, **kwargs)

class Factura_det(models.Model):
	quantity 	 = models.IntegerField(default=0)
	price_sold	 = models.FloatField(default=0, null=True, blank=True)
	total 		 = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=0.00)

	valoracion 	 = models.IntegerField(default=0, null=True, blank=True)
	
	#foreignKeys
	id_factura_fk=models.ForeignKey(
									 Factura,
									  on_delete=models.CASCADE,
									  db_column='id_factura_fk'
									)	
	id_productos_fk=models.ForeignKey(
		 							  Articulo,
		 							   on_delete=models.CASCADE,
		 							   db_column='id_productos_fk',
		 							   null=True, blank=True
		 							 )

	def __str__(self):
		return "numero de factura asociado: " + str(self.id_factura_fk.pk)

class User_credit_card(models.Model):
	serial		= models.CharField(max_length=20) #revisar cantidad de numeros
	cvc			= models.CharField(max_length=3) #revisar cantidad de numeros
	month		= models.IntegerField() 
	year		= models.IntegerField()
	first_name	= models.CharField(max_length=20)
	last_name	= models.CharField(max_length=20)
