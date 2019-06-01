from django.db import models
from home.models import Administrator
from occupant.models import Occupant



class Property(models.Model):
    name = models.CharField(max_length=150)
    address= models.CharField(max_length=250)
    number_of_bedroom = models.DecimalField(max_digits=2, decimal_places=0)
    superficy = models.DecimalField(max_digits=3, decimal_places=0)
    administrator = models.ForeignKey(Administrator,
        on_delete=models.CASCADE,
        related_name='administrator_property',
        verbose_name="related administrator",
    )
    def __str__(self):
        return self.name


class Bedroom(models.Model):
    name = models.CharField(max_length=100)
    occupency = models.BooleanField(default=False)
    superficy = models.DecimalField(max_digits=3, decimal_places=0)
    property = models.ForeignKey(Property,
        on_delete = models.SET_NULL,
        related_name = "property_bedroom",
        verbose_name = "property for bedroom",
        null=True
    )
    def __str__(self):
        return self.name


class Rental(models.Model):
    occupant = models.ForeignKey(Occupant,
        on_delete=models.CASCADE,
        related_name='occupant_rental',
        verbose_name="occupant of rental",
    )
    bedroom = models.ForeignKey(Bedroom,
        on_delete=models.CASCADE,
        related_name='bedroom_rental',
        verbose_name="bedroom for rental",
    )
    rent_amount = models.DecimalField(max_digits=4, decimal_places=0)
    charges = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    property = models.ForeignKey(Property,
        on_delete=models.CASCADE,
        related_name='property_rental',
        verbose_name="property for rental",
    )
    archived = models.BooleanField(default=False)
    #utiliser les chaines de caractères pour importer un modele sans erreur pour les foreign key pour eviter dependances cirulaires"
    def __str__(self):
        return "{} - {} - {}".format(self.occupant, self.rent_amount, self.archived)
