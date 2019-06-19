from django.db import models
from io import BytesIO
import os
from django.core.files import File
from django.dispatch import receiver
from rental.models import Property, Bedroom
from occupant.models import Occupant
from django.conf import settings
from django.contrib.auth.models import User



#pour uploader avec les infos voulues - NON UTILISE CAR GENERE ENVOI DE 2 PDF DANS PDF_CREATION
def quittance_directory_path(instance, filename):
    return 'quittance_{0}_{1}'.format(instance.rental.id, filename)

#RAJOUTER LES CHAMPS PERIODE DE L'ECHEANCE A INDIQUER MANUELLEMENT DANS L'ADMIN
class Quittance(models.Model):
    quittance = models.FileField(upload_to='quittances_pdf/', blank=True)
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

#RAJOUTER LES CHAMPS PERIODE DE L'ECHEANCE A INDIQUER MANUELLEMENT DANS L'ADMIN
class Echeance(models.Model):
    echeance = models.FileField(upload_to='echeances_pdf/', blank=True)
    date_of_issue = models.DateField(blank=True)
    monthly_rent_paid = models.BooleanField(default=False)
    rental = models.ForeignKey(
        "rental.Rental",
        on_delete=models.SET_NULL,
        related_name='rental_echeances',
        verbose_name='related rental',
        null=True
    )
    def __str__(self):
        return "{} - {}".format(self.rental.occupant, self.date_of_issue)

@receiver(models.signals.post_delete, sender=Echeance)
def auto_delete_echeance_on_delete(sender, instance, **kwargs):
    """ Deletes echeance from filesystem when corresponding `MediaFile` object is deleted."""
    if instance.echeance:
        if os.path.isfile(instance.echeance.path):
            os.remove(instance.echeance.path)
