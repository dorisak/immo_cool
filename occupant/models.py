from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver



class TypeDocument(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    def __str__(self):
        return self.name

class Occupant(models.Model):
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='occupant_of',
    )
    is_active = models.BooleanField(default=True)
    date_of_entry = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)
    # doc_id = models.ForeignKey(
    #     Document,
    #     on_delete=models.CASCADE,
    #     verbose_name="Occupant document",
    #     related_name='documents',
    #     blank=True,
    # )
    last_update = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    deposit = models.IntegerField(default='0')
    suivi = models.TextField(max_length=250, blank=True)
    def __str__(self):
        return "{} {}".format(self.user_id.first_name, self.user_id.last_name)


#pour uploader avec les infos voulues
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.occupant_id, filename)

class Document(models.Model):
    occupant_id = models.ForeignKey(Occupant,
        on_delete=models.CASCADE,
        related_name='document_of',
    )
    name = models.CharField(max_length=100)
    uploaded_to = models.FileField(upload_to=user_directory_path, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    type_doc_id = models.ForeignKey(
        TypeDocument,
        on_delete=models.SET_NULL,
        related_name='document_type_of',
        verbose_name="related document type",
        null=True
    )
    def __str__(self):
        return "{} - {} - {}".format(self.occupant_id.user_id.last_name, self.occupant_id.user_id.first_name, self.name)

    # @receiver(models.signals.post_delete, sender=Document)
    # def auto_delete_file_on_delete(sender, instance, **kwargs):
    #     """ Deletes file from filesystem when corresponding `MediaFile` object is deleted."""
    #     if instance.name:
    #         if os.path.isfile(instance.name.path):
    #             os.remove(instance.name.path)
