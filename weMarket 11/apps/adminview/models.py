from django.db import models
from django.utils import timezone


def upload_location(instance, filename):
    return "uploads/%s/img/%s/" % (instance.id, filename) #preguntar a luis

class politics(models.Model):

	conditions = models.TextField(null=True, blank=True)
	cookies = models.TextField(null=True, blank=True)
	privacy = models.TextField(null=True, blank=True)

class indexDesign(models.Model):

	width_field	     = models.IntegerField(default=0, null=True)
	height_field	 = models.IntegerField(default=0, null=True)
	carrousel1 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	carrousel2 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	carrousel3 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	carrousel4 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	title = models.TextField(null=True, blank=True)
	portada  = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)

class contactData(models.Model):

	vision = models.TextField(null=True, blank=True)
	horario = models.TextField(null=True, blank=True)
	width_field	     = models.IntegerField(default=0, null=True)
	height_field	 = models.IntegerField(default=0, null=True)
	image_path	 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	googleMaps = models.TextField(null=True, blank=True)
	mapActivated		 = models.BooleanField(default=True, null=True, blank=True)

class teamMembers(models.Model):
	name = models.TextField(null=True, blank=True)
	position = models.TextField(null=True, blank=True)
	email 			= models.EmailField(max_length=255,unique=True)
	description = models.TextField(null=True, blank=True)
	width_field	     = models.IntegerField(default=0, null=True)
	height_field	 = models.IntegerField(default=0, null=True)
	image_path	 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	existencia		 = models.BooleanField(default=True)


class enterprisedata(models.Model):
	description = models.TextField(null=True, blank=True)
	employees	     = models.IntegerField(default=0)
	name = models.TextField(null=True, blank=True)
	width_field	     = models.IntegerField(default=0, null=True)
	height_field	 = models.IntegerField(default=0, null=True)
	date		= models.DateField(default=timezone.now)
	phone_number	= models.CharField(null=True, blank=True, max_length=13)
	direction		= models.TextField(null=True, blank=True) 
	email 			= models.EmailField(max_length=255,unique=True)
	logo	 = models.ImageField(
										upload_to=upload_location,
									    null=True, blank=True, 
										width_field="width_field", 
										height_field="height_field"
									)
	copyright = models.TextField(null=True, blank=True)
	def __str__(self):
		return "("+str(self.id)+") " + self.template_name

class Templates(models.Model):
	description 	= models.TextField(null=True, blank=True)
	template_name 	= models.TextField(null=True, blank=True)
	isSelected		= models.BooleanField(default=False)
	temp_selected	= models.BooleanField(default=False)
	width_field	     = models.IntegerField(default=0, null=True)
	height_field	 = models.IntegerField(default=0, null=True)
	image_path	 	= models.ImageField(
										width_field="width_field", 
										height_field="height_field"
									)
	def __str__(self):
		return "("+str(self.id)+") " + self.template_name

class Available_design_page(models.Model):
	name 			= models.TextField(null=True, blank=True)
	type_design 	= models.TextField(null=True, blank=True)
	description 	= models.TextField(null=True, blank=True)
	isSelected		= models.BooleanField(default=False)
	temp_selected	= models.BooleanField(default=False)
	width_field	     = models.IntegerField(default=0, null=True)
	height_field	 = models.IntegerField(default=0, null=True)
	image_path	 	= models.ImageField(
										width_field="width_field", 
										height_field="height_field"
									)
	image_path1	 = models.ImageField(
										width_field="width_field", 
										height_field="height_field"
									)
	image_path2	 = models.ImageField(
										width_field="width_field", 
										height_field="height_field"
									)
	def __str__(self):
		return "("+str(self.id)+") " + self.name

