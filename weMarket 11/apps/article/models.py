from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.myuser.models import CustomUser
from django.utils import timezone


def upload_location(instance, filename):
    return "uploads/%s/img/%s/" % (instance.id, filename) #preguntar a luis

# Create your models here.
class Clasificacion(models.Model):
	nombre_clasificacion = models.CharField(max_length=64)
	descripcion = models.CharField(max_length=300, null=True, blank=True)
	existencia			 = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre_clasificacion
		
class Articulo(models.Model):
	precio			 = models.FloatField(default=1, validators=[MinValueValidator(1, message='Tiene que ser mayor a 0')])
	cantidad		 = models.IntegerField(default=1, validators=[MinValueValidator(1, message='Tiene que ser mayor a 0')])
	existencia		 = models.BooleanField(default=True)
	agotado			 = models.BooleanField(default=False)
	valoracion		 = models.IntegerField(default=0)
	Descripcion 	 = models.TextField(null=True, blank=True)
	nombre_producto	 = models.CharField(max_length=64)
	long_descripcion = models.TextField(null=True, blank=True)

	width_field	     = models.IntegerField(default=0)
	height_field	 = models.IntegerField(default=0)
	nombre_imagen	 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	#llaves 
	id_clasificacion_fk=models.ForeignKey(Clasificacion, null=True, blank=True, on_delete=models.CASCADE, db_column='id_clasificacion_fk')

	def __str__(self):
		return "("+str(self.id)+") " + self.nombre_producto

class Comment(models.Model):

	contenido = models.TextField(null=True, blank=True)
	asunto = models.TextField(null=True, blank=True)
	fecha = models.DateTimeField(default=timezone.now)
	existencia		 = models.BooleanField(default=True)

	#llaves 
	id_article_fk=models.ForeignKey(Articulo, null=True, blank=True, on_delete=models.CASCADE, db_column='id_article_fk')
	id_user_fk=models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, db_column='id_user_fk')

