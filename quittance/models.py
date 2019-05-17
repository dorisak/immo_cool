from django.db import models
from rental.models import Property, Bedroom
from occupant.models import Occupant
from django.conf import settings
from django.contrib.auth.models import User



class Quittance(models.Model):
    #RENOMMER LES CHAMPS AVEC ID SANS LE MOT ID
    property_id = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='property',
        verbose_name="related property",
    )
    occupant_id = models.ForeignKey(
        Occupant,
        on_delete=models.CASCADE,
        related_name='occupant',
        verbose_name="related occupant",
    )
    date = models.DateField()
    bedroom_id = models.ForeignKey(
        Bedroom,
        on_delete=models.CASCADE,
        related_name='bedroom',
        verbose_name="related bedroom",
    )
    monthly_rent_paid = models.BooleanField(default=False)
    date_of_payment = models.DateField()
    def __str__(self):
        return "{} - {} - {}".format(self.Occupant.first_name, self.Occupant.last_name, self.date)
