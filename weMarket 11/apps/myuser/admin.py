from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class BaseUserAdmin(UserAdmin):

	form = UserChangeForm
	add_form = UserCreationForm

	model = CustomUser

	list_display = ('email',  'is_active', 'is_staff','is_superuser')
	list_filter = ('email', 'is_staff', 'is_active', 'is_staff')
	fieldsets = (
	('Username and password (you are using email address like username)', {'fields': ('email', 'password')}),
	('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth','phone_number', 'direction')}),
	('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
	)

	add_fieldsets = (
	(None, {
	'classes': ('wide',),
	'fields': ( 'email','first_name', 'last_name', 'password1', 'password2',
				 'date_of_birth','phone_number', 'direction', 
				'is_staff','is_superuser')}
	),
	)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(CustomUser, BaseUserAdmin)
