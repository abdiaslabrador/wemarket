from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser

#esto la clase madre que hereda UserRegisterForm-------------------

class PhotoUserForm(forms.ModelForm):

	class Meta:
		model = CustomUser
		fields = [
					"photo",
					]

class UserCreationForm(forms.ModelForm):

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


	class Meta:
		model = CustomUser
		fields = (
					"email",
				  )

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Contraseñas no coinciden")
		return password2


	def save(self, commit=True):
	# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	#A form for updating users. Includes all the fields on
	#the user, but replaces the password field with admin's
	#password hash display field.
	
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CustomUser
		fields = ('email', 'password')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

#esto es para el formulario de registro de un usuario--------------------------
class RegisterForm(UserCreationForm):

	class Meta:
		model=CustomUser
		fields = (
					'first_name',
					'last_name',
					'email',
					'phone_number',
					'date_of_birth',
					'direction',
					
				 )

class UserConfigurationForm(UserChangeForm):

	class Meta:
		model=CustomUser
		fields = (
					'first_name',
					'last_name',
					'email',
					'phone_number',
					'direction',
					'password',
					'photo',
				 )

#esto es para el formulario del login-----------------
class LoginForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	

	class Meta:
		model=CustomUser
		fields = (
					'email',
					'password',
				 )

	
	def clean(self):
		# Check that the email and password will be correct
		cleaned_data=super().clean()

		email = cleaned_data.get("email")
		password = cleaned_data.get("password")

		
		try:
			user=CustomUser.objects.get(email=email)
		except CustomUser.DoesNotExist:
			raise forms.ValidationError("El correo no existe.")
		else:
			if user.check_password(password) is not True:
				raise forms.ValidationError("Contraseña inválida.")

		return cleaned_data

