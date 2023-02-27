from django import forms
from .models import User_credit_card, Factura_det




class User_credit_cardForm(forms.ModelForm):

    class Meta:
        model = User_credit_card
        fields = [
            'serial',
            'cvc',
            'month',
            'year',
            'first_name',
            'last_name',
            ]

class valoracionForm(forms.ModelForm):

    class Meta:
        model = Factura_det
        fields = [
            'valoracion',
            ]
				
			
		