from django.apps import AppConfig
from django.db import models

class ArticleConfig(AppConfig):
    name = 'article'



# Create your models here.
class Articulo(models.Model):
	nombre_producto= models.CharField(max_length=64)
	Descripcion= models.TextField(null=True, blank=True)
	precio=models.FloatField()
	cantidad=models.IntegerField()
	existencia=models.BooleanField(default=True)
	nombre_imagen=models.ImageField(max_length=64)
	#llaves 
	id_clasificacion_fk=models.ForeignKey('Clasificacion', null=True, blank=True, on_delete=models.CASCADE, db_column='id_clasificacion_fk')

	def __str__(self):
		return self.nombre_producto	

class Clasificacion(models.Model):
	nombre_clasificacion= models.CharField(max_length=64)
	existencia=models.BooleanField(default=True)

	def __str__(self):
		return self.nombre_clasificacion
