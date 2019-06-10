""" Create a quittance each month for each occupant """
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from rental.models import Rental
from quittance.models import Quittance
from django.shortcuts import get_object_or_404
from io import BytesIO
import datetime
import tempfile


help = 'Create a quittance each month for each occupant'


class Command(BaseCommand):
    """ GET the quittance for each occupant """

    def handle(self, *args, **options):
        rentals = Rental.objects.filter(archived=False)
        today = datetime.date.today()
        current_month = _(today.strftime('%B'))


        for rental in rentals:
            try:
                id = rental
                name = slugify(rental.occupant)
                date = today.strftime('%Y-%m-%d')
                sum_rent = rental.charges+rental.rent_amount
                occupant_email = rental.occupant.user.email
                filename = '{}-{}.pdf'.format(date, name)

                html_string = render_to_string("quittance/quittance_base.html", {
                    'rentals': rental,
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
                    stored_quittance.date_of_issue = today
                    stored_quittance.rental = id
                    saved_quittance = stored_quittance.quittance.save(filename, django_file, save=True)
                    self.stdout.write('Occupant %s will receive the quittance %s' % (rental.occupant, filename))

                    try:
                        occupant_name = rental.occupant.user.last_name
                        occupant_firstname = rental.occupant.user.first_name
                        admin_name = rental.administrator.user.last_name
                        admin_firstname = rental.administrator.user.first_name
                        message = "Bonjour {} {} - Vous trouverez ci-joint la quittance de loyer pour {}; Cordialement, {} {}".format(
                            occupant_name, occupant_firstname, current_month, admin_firstname, admin_name
                        )
                        email_from = settings.EMAIL_HOST_USER
                        email = EmailMessage(
                            'Quittance de loyer', message, email_from,
                            [occupant_email],)
                        email.attach_file(stored_quittance.quittance.path)
                        email.send(fail_silently=False)
                        self.stdout.write("Le mail pour {} a bien été envoyé".format(rental.occupant))
                    except Rental.DoesNotExist:
                        self.stdout.write("Le mail pour {} n\'a pas pu être envoyé".format(rental.occupant))

            except Rental.DoesNotExist:
                self.stdout.write('Occupant "%s" does not exist.' % rental.occupant)
