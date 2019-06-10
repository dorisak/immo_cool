# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.core.mail import mail_admins
from datetime import datetime, date
from quittance.models import Quittance
from django.conf import settings
from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger = logging.getLogger()
        today = date.today()
        current_month = today.month
        current_year = today.year

        in_late = Quittance.objects.filter(
            date_of_issue__gt = date(current_year, current_month, 2),
            monthly_rent_paid = False
        )
        for people in in_late:
            try:
                occupant = people.rental.occupant
                property = people.rental.property
                message = "{} - Le locataire {} n'a pas encore réglé son loyer pour le mois {}".format(
                    property, occupant, current_month
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['doris.atchikiti@gmail.com',]

                email = send_mail(
                    fail_silently=False,
                    subject = 'Alerte - loyer en retard',
                    message = message,
                    from_email = email_from,
                    recipient_list = recipient_list
                )

            except Quittance.DoesNotExist:
                self.stdout.write('Pas de quittances impayées')
