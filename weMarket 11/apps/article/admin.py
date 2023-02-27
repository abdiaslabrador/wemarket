from django.contrib import admin
from apps.article.models import Articulo, Clasificacion
# Register your models here.
admin.site.register(Articulo)
admin.site.register(Clasificacion)