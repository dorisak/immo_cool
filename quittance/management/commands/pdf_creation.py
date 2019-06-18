""" Create a quittance each month for each occupant """
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
from quittance.models import Quittance
from io import BytesIO
import datetime
import tempfile


help = 'Create a quittance each month for each occupant'


class Command(BaseCommand):
    """ GET the quittance for each occupant """

    def handle(self, *args, **options):
        rentals = Quittance.objects.filter(monthly_rent_paid=False, rental__archived=False)
        today = datetime.date.today()
        current_month = _(today.strftime('%B'))

        for item in rentals:
            try:
                id = item.rental
                name = slugify(item.rental.occupant)
                date = today.strftime('%Y-%m-%d')
                sum_rent = item.rental.charges+item.rental.rent_amount
                occupant_email = item.rental.occupant.user.email
                filename = '{}-{}.pdf'.format(date, name)

                html_string = render_to_string("quittance/quittance_base.html", {
                    'rentals': item,
                    'today': today,
                    'sum_rent': sum_rent,
                })
                html = HTML(string=html_string)
                with tempfile.TemporaryDirectory() as tmpdirname:
                    result = html.write_pdf(target='{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename))

                    quittance_to_store = open('{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename), 'rb+')
                    # Convert it to a Django File.
                    django_file = File(quittance_to_store)
                    stored_quittance = Quittance()
                    item.date_of_issue = today
                    item.rental = id
                    saved_quittance = item.quittance.save(filename, django_file, save=True)
                    self.stdout.write(self.style.SUCCESS('Occupant {} will receive the quittance {}'.format(item.rental.occupant, filename)))

                    try:
                        occupant_name = item.rental.occupant.user.last_name
                        occupant_firstname = item.rental.occupant.user.first_name
                        admin_name = item.rental.property.administrator.user.last_name
                        admin_firstname = item.rental.property.administrator.user.first_name
                        message = "Bonjour {} {} - Vous trouverez ci-joint la quittance de loyer pour {}; Cordialement, {} {}".format(
                            occupant_name, occupant_firstname, current_month, admin_firstname, admin_name
                        )
                        email_from = settings.EMAIL_HOST_USER
                        email = EmailMessage(
                            'Quittance de loyer', message, email_from,
                            [occupant_email],)
                        email.attach_file(item.quittance.path)
                        email.send(fail_silently=False)
                        self.stdout.write(self.style.SUCCESS("Le mail pour {} a bien été envoyé".format(item.rental.occupant)))
                    except Rental.DoesNotExist:
                        self.stdout.write(self.style.WARNING("Le mail pour {} n\'a pas pu être envoyé".format(item.rental.occupant)))

            except Rental.DoesNotExist:
                self.stdout.write(self.style.WARNING('Occupant "{}" does not exist.'.format(item.rental.occupant)))
