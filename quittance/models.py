from django.db import models
from io import BytesIO
import os
from django.core.files import File
from django.dispatch import receiver
from rental.models import Property, Bedroom
from occupant.models import Occupant
from django.conf import settings
from django.contrib.auth.models import User



#pour uploader avec les infos voulues
def quittance_directory_path(instance, filename):
    return 'quittance_{0}_{1}'.format(instance.rental.id, filename)

class Quittance(models.Model):
    quittance = models.FileField(upload_to=quittance_directory_path, blank=True)
    monthly_rent_paid = models.BooleanField(default=False)
    date_of_issue = models.DateField(blank=True)
    rental = models.ForeignKey(
        "rental.Rental",
        on_delete=models.SET_NULL,
        related_name='rental_quittances',
        verbose_name='related rental',
        null=True
    )
    def __str__(self):
        return "{} - {}".format(self.rental.occupant, self.date_of_issue)

@receiver(models.signals.post_delete, sender=Quittance)
def auto_delete_quittance_on_delete(sender, instance, **kwargs):
    """ Deletes quittance from filesystem when corresponding `MediaFile` object is deleted."""
    if instance.quittance:
        if os.path.isfile(instance.quittance.path):
            os.remove(instance.quittance.path)
