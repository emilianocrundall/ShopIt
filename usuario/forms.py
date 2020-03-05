from django.contrib.auth.models import User
from django import forms

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields= [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form_input'}),
            'first_name': forms.TextInput(attrs={'class': 'form_input'}),
            'last_name': forms.TextInput(attrs={'class': 'form_input'}),
            'email': forms.EmailInput(attrs={'class': 'form_input'}),
            'password': forms.PasswordInput(attrs={'class': 'form_input'})
        }