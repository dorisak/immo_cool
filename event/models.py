from django.db import models



class TypeEventEcheance(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name)

class EventEcheance(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField()
    description = models.TextField(max_length=250)
    type = models.ForeignKey(TypeEventEcheance,
    on_delete=models.SET_NULL,
    verbose_name="type of event",
    related_name="type_event",
    null=True)
    def __str__(self):
        return "{} - {} - {}".format(self.name, self.description, self.type)
