from django.contrib import admin

# Register your models here.
from apps.factura.models import Factura, Factura_det
# Register your models here.
admin.site.register(Factura)
admin.site.register(Factura_det)