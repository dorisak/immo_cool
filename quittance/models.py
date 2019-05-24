from django.db import models
from rental.models import Property, Bedroom
from occupant.models import Occupant
from django.conf import settings
from django.contrib.auth.models import User


#pour uploader avec les infos voulues
def quittance_directory_path(instance, filename):
    return 'quittance_{0}/{1}/{2}'.format(instance.quittance, filename, occupant)

class Quittance(models.Model):
    #RENOMMER LES CHAMPS AVEC ID SANS LE MOT ID
    quittance = models.FileField(upload_to=quittance_directory_path, blank=True)
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='property',
        verbose_name="related property",
    )
    occupant = models.ForeignKey(
        Occupant,
        on_delete=models.CASCADE,
        related_name='occupant',
        verbose_name="related occupant",
    )
    date = models.DateField()
    bedroom = models.ForeignKey(
        Bedroom,
        on_delete=models.CASCADE,
        related_name='bedroom',
        verbose_name="related bedroom",
    )
    monthly_rent_paid = models.BooleanField(default=False)
    date_of_payment = models.DateField()
    rental = models.ForeignKey(
        "rental.Rental",
        on_delete=models.SET_NULL,
        related_name='rental_quittances',
        verbose_name='related rental',
        null=True
    )
    def __str__(self):
        return "{} - {}".format(self.occupant, self.date)
