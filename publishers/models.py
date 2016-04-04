from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import datetime

def validate_date_higher_today(value):
    today = datetime.datetime.now()
    if today.strftime('%Y-%m-%d') >= value.strftime('%Y-%m-%d'):
        raise ValidationError('La Fecha No Puede ser Menor Ni Igual a Hoy')

#def validate_unique_date(value):


TYPES = (
    ('text', 'Texto'),
    ('image', 'Imagen'),
    ('video', 'Video'),
    ('page', 'Pagina'),
)

class Publishers(models.Model):
    content = models.TextField(verbose_name='Contenido de la Publicaciòn')
    type = models.CharField(max_length=10, choices=TYPES, verbose_name='Tipo de Publicaciòn')
    link = models.URLField(blank=True, verbose_name='Direccón del Enlace')
    state  = models.BooleanField(default=False)
    start = models.BooleanField(default=False)
    ends = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.content
    def __str__(self):
        return self.content


class Dates(models.Model):
    date = models.DateField(verbose_name='Fecha de Publicaciòn', validators=[validate_date_higher_today])
    state = models.BooleanField(default=False)
    publisher = models.ForeignKey(Publishers)