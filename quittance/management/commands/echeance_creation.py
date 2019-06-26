""" Create an echeance if the rent is not paid """
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files import File
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from rental.models import Rental
from quittance.models import Echeance
from io import BytesIO
import datetime
import tempfile


help = 'Create an echeance if the rent is not paid'


class Command(BaseCommand):
    """ GET the echeance for each rent unpaid """

    def handle(self, *args, **options):
        echeance = Echeance.objects.filter(monthly_rent_paid=False, rental__archived=False)
        today = datetime.date.today()
        current_month = _(today.strftime('%B'))

        for item in echeance:
            try:
                id = item.rental
                name = slugify(item.rental.occupant)
                date = today.strftime('%Y-%m-%d')
                sum_rent = item.rental.charges+item.rental.rent_amount
                occupant_email = item.rental.occupant.user.email
                filename = '{}-{}.pdf'.format(date, name)

                html_string = render_to_string("quittance/echeance_base.html", {
                    'rentals': id,
                    'today': today,
                    'sum_rent': sum_rent,
                })
                html = HTML(string=html_string)
                with tempfile.TemporaryDirectory(dir=settings.MEDIA_ROOT) as tmpdirname:
                    #PAS UTILE enregistrer dans le Mediaroot/echeance_pdf
                    #PAS UTILE prefix=settings.MEDIAROOT/echeance_pdf/tmp 
		    self.stdout.write(tmpdirname)
		    self.stdout.write(gettempdir)
                    result = html.write_pdf(target='{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename))
	
                    echeance_to_store = open('{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename), 'rb+')
                    # Convert it to a Django File.
                    django_file = File(echeance_to_store)
                    stored_echeance = Echeance()
                    item.date_of_issue = today
                    item.rental = id
                    saved_echeance = item.echeance.save(filename, django_file, save=True)
                    self.stdout.write(self.style.SUCCESS("Le locataire {} recevra l\n'écheance {}".format(item.rental.occupant, filename)))

                    try:
                        occupant_name = item.rental.occupant.user.last_name
                        occupant_firstname = item.rental.occupant.user.first_name
                        admin_name = item.rental.property.administrator.user.last_name
                        admin_firstname = item.rental.property.administrator.user.first_name
                        message = "Bonjour {} {}, \nVous trouverez ci-joint l'avis d'échéance de loyer pour {}. Il sera à régler dans les délais prévus dans votre contrat de location. \nSi vous avez déjà réglé votre loyer entretemps pour cette période, merci de ne pas tenir compte de ce mail. \nCordialement, \n{} {}".format(
                            occupant_firstname, occupant_name, current_month, admin_firstname, admin_name
                        )
                        email_from = settings.EMAIL_HOST_USER
                        email = EmailMessage(
                            "Avis d\'échéance de loyer", message, email_from,
                            [occupant_email],)
                        email.attach_file(item.echeance.path)
                        email.send(fail_silently=False)
                        self.stdout.write(self.style.SUCCESS("Le mail pour {} a bien été envoyé".format(item.rental.occupant)))
                    except Echeance.DoesNotExist:
                        self.stdout.write(self.style.WARNING("Le mail pour {} n\'a pas pu être envoyé".format(item.rental.occupant)))

            except Exception as e:
                self.stdout.write(self.style.WARNING(e))
