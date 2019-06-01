from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Administrator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='administrator_of',
    )
    address = models.CharField(max_length=250, default='None')
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
