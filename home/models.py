from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Administrator(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='administrator_of',
    )
    def __str__(self):
        return "{} {}".format(self.user_id.first_name, self.user_id.last_name)
