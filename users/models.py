from django.db import models

from django.contrib.auth.models import User

class ActivationCode(models.Model):
    code = models.CharField(max_length=100)
    send_time = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)
    description = models.CharField(max_length=20, default='Create')
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.user.username

COUNTRIES = (
    ('Bolivia', 'Bolivia'),
    ('Argentina', 'Argentina'),
)

class Person(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombres')
    surnames = models.CharField(max_length=50, verbose_name='Apellidos')
    country = models.CharField(max_length=20, verbose_name='País', choices=COUNTRIES)
    cellphone = models.IntegerField(verbose_name='Celular')
    phono = models.IntegerField(verbose_name='Telefono')
    address = models.CharField(max_length=50, verbose_name='Dirección')
    user = models.OneToOneField(User, default=1)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name