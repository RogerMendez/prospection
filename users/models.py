from django.db import models

from django.contrib.auth.models import User

class ActivationCode(models.Model):
    code = models.CharField(max_length=100)
    send_time = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.user.username