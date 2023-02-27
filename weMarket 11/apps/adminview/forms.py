from django import forms
from apps.article.models import Clasificacion, Articulo
from apps.adminview.models import enterprisedata, contactData, indexDesign, teamMembers, politics
from apps.myuser.models import CustomUser
from apps.factura.models import Factura

class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('/css/pretty.css',),
        }
        js = ('jQuery.js', 'calendar.js', 'noConflict.js')

class IndexForm(forms.ModelForm):

    class Meta:
        model = indexDesign
        fields = [
            'portada',
            'carrousel1',
            'carrousel2',
            'carrousel3',
            'carrousel4',
            'title',
        ]

class ContactForm(forms.ModelForm):

    mapActivated = forms.BooleanField(required=False)
    class Meta:
        model = contactData
        fields = [
            'vision',
            'horario',
            'image_path',
            'mapActivated',
            ]
        labels = {
            'image_path': '',    
        }

class EnterpriseForm(forms.ModelForm):

    class Meta:
        model = enterprisedata
        date = forms.DateField(widget=CalendarWidget)
        fields = [
            'name',
            'description',
            'direction',
            'phone_number',
            'email',
            'date',
            'employees',
            'logo',
            'copyright',
            ]
            
        labels = {
            'name': 'Nombre de la empresa',
            'description': 'Descripción de la empresa',
            'direction': 'Dirección',
            'phone_number': 'Número telefónico',
            'email': 'Correo Electrónico',
            'date': 'Fecha de fundación',
            'employees': 'Número de empleados (Aproximado)',
            'logo': 'Logo de la empresa',    
        }
        
        widgets = {

        }

class PoliticsForm(forms.ModelForm):

    class Meta:
        model = politics

        fields = [

            'conditions',
            'cookies',
            'privacy',
            ]

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Articulo

        fields = [
            'nombre_producto',
            'id_clasificacion_fk',
            'Descripcion',
            'long_descripcion',
            'precio',
            'cantidad',
            'nombre_imagen',
            'agotado',
            ]
        labels = {
            'nombre_producto': 'Nombre del producto',
            'id_clasificacion_fk': 'Clasificación del producto',
            'Descripcion': 'Corta descipción',
            'long_descripcion': 'Larga descipción',
            'precio': 'Precio del producto',
            'cantidad': 'Cantidad en inventario',
            'nombre_imagen' : 'selecione una imagen',
        }
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class':'form-control'}),
            'id_clasificacion_fk': forms.Select(attrs={'class':'form-control'}),
            'Descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'long_descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(),
            'cantidad': forms.NumberInput(),
            
        }
        
class MemberForm(forms.ModelForm):

    class Meta:
        model = teamMembers
        fields = [
            'image_path',
            'name',
            'position',
            'description',
            'email',
            ]

class UserForm(forms.ModelForm):
    ROL = (('Corriente', 'Corriente'),('Moderador', 'Moderador'),('Administrador', 'Administrador'),)
    rol = forms.ChoiceField(choices=ROL)

    class Meta:
        model = CustomUser
        
        fields = [
            'email',
            'first_name',
            'last_name',
            'direction',
            'phone_number',
            ]
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'direction':'Dirección',
        }

class ClasificacionForm(forms.ModelForm):

    class Meta:
        model = Clasificacion

        fields = [
            'nombre_clasificacion',
            'descripcion',
            ]
        labels = {
            'nombre_clasificacion': '',
            'descripcion': 'Descripción de la categoría',
        }
        widgets = {
            'nombre_clasificacion': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'})
        }

class admin_givenForm(forms.ModelForm):

    class Meta:
        model = Factura

        fields = [
            'entregado',
            ]