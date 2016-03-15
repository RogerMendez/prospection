from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from users.models import Person

class EmailForm(forms.Form):
    email = forms.EmailField(label='Correo Electronico', widget=forms.TextInput(attrs={'type':'email'}))
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Correo Electronico Registrado")
        return data

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ['user']