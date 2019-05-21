from django.db import models
from home.models import Administrator
from occupant.models import Occupant



class Bedroom(models.Model):
    name = models.CharField(max_length=100)
    occupency = models.BooleanField(default=False)
    superficy = models.DecimalField(max_digits=3, decimal_places=0)
    def __str__(self):
        return "{} - {}".format(self.occupency, self.name)

class Property(models.Model):
    name = models.CharField(max_length=150)
    address= models.CharField(max_length=250)
    number_of_bedroom = models.DecimalField(max_digits=2, decimal_places=0)
    superficy = models.DecimalField(max_digits=3, decimal_places=0)
    bedroom_id = models.ForeignKey(Bedroom,
        on_delete=models.CASCADE,
        related_name='bedroom_property',
        verbose_name="bedroom in property",
    )
    administrator_id = models.ForeignKey(Administrator,
        on_delete=models.CASCADE,
        related_name='administrator_property',
        verbose_name="related administrator",
    )
    def __str__(self):
        return "{} - {}".format(self.name, self.administrator_id)

class Rental(models.Model):
    occupant_id = models.ForeignKey(Occupant,
        on_delete=models.CASCADE,
        related_name='occupant_rental',
        verbose_name="occupant of rental",
    )
    bedroom_id = models.ForeignKey(Bedroom,
        on_delete=models.CASCADE,
        related_name='bedroom_rental',
        verbose_name="bedroom for rental",
    )
    rent_amount = models.DecimalField(max_digits=4, decimal_places=0)
    property_id = models.ForeignKey(Property,
        on_delete=models.CASCADE,
        related_name='property_rental',
        verbose_name="property for rental",
    )
    archived = models.BooleanField(default=False)
    quittance_id = models.ForeignKey("quittance.Quittance",
        on_delete=models.CASCADE,
        related_name='quittance_rental',
        verbose_name="quittance for rental",
        null=True,
        blank=True,
    )
    #utiliser les chaines de caractères pour importer un modele sans erreur pour les foreign key pour eviter dependances cirulaires"
    def __str__(self):
        return "{} - {} - {}".format(self.occupant_id, self.rent_amount, self.archived)
