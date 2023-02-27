from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation  import validate_password
from django.db.models.signals import pre_save, post_save

def upload_location(instance, filename):
    return "uploads/%s/img/%s/" % (instance.id, filename) #preguntar a luis

class UserManager(BaseUserManager):
	#Change the password for any user
	def change_password(self, email, password):

		if not email:
			raise ValueError('Los usuarios tienen que tener email')
		if not password:
			raise ValueError('Los usuarios tienen que tener contraseña')
		
		try:
			user = self.model.objects.get(email=email)
		except self.model.DoesNotExist:
			raise ValueError('Correo no encontrado')

		try: 
			validate_password(password)
		except:
			raise ValueError('La contraseña cumple con los requerimientos')
		user.set_password(password)

		user.save(using=self._db)
		return user

	def create_user(self, email, first_name, last_name, password=None):

		if not email:
			raise ValueError('Los usuarios tienen que tener email')
		if not password:
			raise ValueError('Los usuarios tienen que tener contraseña')
		if not first_name:
			raise ValueError('Los usuarios tienen que tener primer nombre')

		
		user = self.model(  email=self.normalize_email(email),
							first_name=first_name,
							last_name=last_name,
						  )
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, first_name, last_name, password):

		user =self.create_user(email,
							    password=password,
							    first_name=first_name,
							    last_name=last_name,
							   )
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user
    	
class CustomUser(AbstractBaseUser, PermissionsMixin):
	ROL = (
			('Corriente', 'Corriente'),
			('Moderador', 'Moderador'),
			('Administrador', 'Administrador'),
		)
	
	email 			= models.EmailField(max_length=255,unique=True) #username

	is_active		= models.BooleanField(default=True)
	is_staff		= models.BooleanField(default=False)#pendiente probar

	rol		= models.CharField(default="Corriente", max_length=500, choices=ROL)

	date_joined		= models.DateTimeField(default=timezone.now)
	
	first_name		= models.CharField(null=False, blank=False, max_length=20)
	last_name		= models.CharField(null=False, blank=False, max_length=20)

	date_of_birth	= models.DateField(null=True, blank=False)

	money			= models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2, default=10000.00)

	direction		= models.TextField(null=True, blank=False) 
	phone_number	= models.CharField(null=True, blank=False, max_length=13)

	width_field	    = models.IntegerField(default=0, null=True)
	height_field	= models.IntegerField(default=0, null=True)

	photo	 		= models.ImageField(

										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)

	USERNAME_FIELD	= 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']
	
	objects = UserManager()
	#this two funtions below are inherited from AbstractBaseUser--

	
	def get_full_name(self):
		return str(self.first_name + " " + self.first_name)

	def get_short_name(self):
		return self.first_name	

	def __str__(self):
		return self.email

	def has_module_perms(self, app_label):
		return True

	def has_perm(self, perm, obj=None):
		return True

