""" Create a quittance each month for each occupant """

# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from io import BytesIO
from django.core.files import File
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from rental.models import Rental
from quittance.models import Quittance
from django.shortcuts import get_object_or_404
import datetime
import tempfile


help = 'Create a quittance each month for each occupant'


class Command(BaseCommand):
    """ GET the quittance for each occupant """

    def handle(self, *args, **options):
        rentals = Rental.objects.filter(archived=False)
        today = datetime.date.today()

        for rental in rentals:
            try:
                id = rental
                name = slugify(rental.occupant)
                date = today.strftime('%Y-%m-%d')
                sum_rent = rental.charges+rental.rent_amount
                filename = '{}-{}-quittance.pdf'.format(date, name)
                # response = HttpResponse(content_type="application/pdf")
                # response['Content-Disposition'] = "attachement; filename= {}".format(filename)

                html_string = render_to_string("quittance/quittance_base.html", {
                    'rentals': rental,
                    'today': today,
                    'sum_rent': sum_rent,
                })
                html = HTML(string=html_string)
                with tempfile.TemporaryDirectory() as tmpdirname:
                    result = html.write_pdf(target='{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename))

                    test = open('{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename), 'rb+')
                    # Convert it to a Django File.
                    django_file = File(test)
                    stored_quittance = Quittance()
                    stored_quittance.date_of_issue = today
                    stored_quittance.rental = id
                    stored_quittance.quittance.save(filename, django_file, save=True)

                     # with tmpdirname.open() as pdf:
                # if result != None:
                #     quittance_saved = Quittance(
                #         quittance = result,
                #         date_of_issue = today,
                #         rental = id
                #     )
                #     quittance_saved.save()
                    self.stdout.write('Occupant %s will receive the quittance %s' % (rental.occupant, filename))
                # else:
                #     self.stdout.write('Quittance for %s could not be generated' % rental.occupant)

            except Rental.DoesNotExist:
                self.stdout.write('Occupant "%s" does not exist.' % rental.occupant)
