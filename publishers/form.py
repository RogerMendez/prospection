from django import forms
from django.forms import ModelForm, Textarea, TextInput

from publishers.models import Publishers, Dates

import datetime

class PublishersForm(ModelForm):
    class Meta:
        model = Publishers
        exclude = ['state', 'start', 'ends', 'user']
        widgets = {
            'content': Textarea(attrs={'rows': '3'}),
        }


class DatesForm(ModelForm):
    class Meta:
        model = Dates
        exclude = ['publisher', 'state']
        widgets = {
            'date': TextInput(attrs={'type': 'date'}),
        }
    def clean_date(self):
        today = datetime.datetime.now()
        data = self.cleaned_data['date']
        if today.strftime('%Y-%m-%d') == data.strftime('%Y-%m-%d'):
            raise forms.ValidationError("No se Puede Agregar Fechas Menoras A la Actual")
        return data