from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver



class TypeDocument(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

#pour uploader avec les infos voulues
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.User.id, filename)

class Document(models.Model):
    occupant_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        return "{} - {} - {}".format(self.User.first_name, self.User.last_name, self.name)

    # @receiver(models.signals.post_delete, sender=Document)
    # def auto_delete_file_on_delete(sender, instance, **kwargs):
    #     """ Deletes file from filesystem when corresponding `MediaFile` object is deleted."""
    #     if instance.name:
    #         if os.path.isfile(instance.name.path):
    #             os.remove(instance.name.path)


class Occupant(models.Model):
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='occupant_of',
    )
    is_active = models.BooleanField()
    date_of_entry = models.DateField()
    date_of_leaving = models.DateField()
    doc_id = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        verbose_name="related document",
        related_name='documents',
    )
    last_update = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    deposit = models.IntegerField()
    suivi = models.TextField(max_length=250)
    def __str__(self):
        return "{} - {}".format(self.first_name, self.last_name)
