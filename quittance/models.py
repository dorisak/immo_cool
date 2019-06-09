from django.db import models
from io import BytesIO
from django.core.files import File
# from .commands import handle
from rental.models import Property, Bedroom
from occupant.models import Occupant
from django.conf import settings
from django.contrib.auth.models import User



#pour uploader avec les infos voulues
def quittance_directory_path(instance, filename):
    return 'quittance_{0}_{1}'.format(instance.quittance, filename)

class Quittance(models.Model):
    quittance = models.FileField(upload_to=quittance_directory_path, blank=True)
    # property = models.ForeignKey(
    #     Property,
    #     on_delete=models.CASCADE,
    #     related_name='property',
    #     verbose_name="related property",
    # )
    # occupant = models.ForeignKey(
    #     Occupant,
    #     on_delete=models.CASCADE,
    #     related_name='occupant',
    #     verbose_name="related occupant",
    # )
    # bedroom = models.ForeignKey(
    #     Bedroom,
    #     on_delete=models.CASCADE,
    #     related_name='bedroom',
    #     verbose_name="related bedroom",
    # ) A SUPPRIMER ET SURTOUT VOIR SI JE PEUX FAIRE APPEL A LA FK RENTAL POUR AFFICHER CES INFOS
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

        # to generate and save your pdf to your model
    def generate_obj_pdf(instance_id):
         obj = Quittance.objects.get(id=instance_id)
         context = {'instance': obj}
             # pdf = render_to_pdf('quittance/quittance_base.html', context)
         filename = '{}-{}-quittance.pdf'.format(rental.date, rental.name)
         obj.pdf.save(filename, File(BytesIO(pdf.content)))
