# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date
from quittance.models import Echeance
from django.conf import settings
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send email alerts to Administrators when an occupant hasn\'t paid its rent'

    def handle(self, *args, **options):
        # logger = logging.getLogger()
        today = date.today()
        current_month = today.month
        current_month_format = _(today.strftime('%B'))
        current_year = today.year

        in_late = Echeance.objects.filter(
            date_of_issue__gt = date(current_year, current_month, 2),
            monthly_rent_paid = False
        )
        for people in in_late:
            try:
                occupant = people.rental.occupant
                property = people.rental.property
                message = "{} - Le locataire {} n'a pas encore réglé son loyer pour {}".format(
                    property, occupant, current_month_format
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['datxik@gmail.com',]

                email = send_mail(
                    fail_silently=False,
                    subject = 'Alerte - loyer en retard',
                    message = message,
                    from_email = email_from,
                    recipient_list = recipient_list
                )
                self.stdout.write(self.style.SUCCESS("L'alerte administrateur a bien été envoyée pour le loyer en retard de {} en date du {}-{}".format(occupant, current_month, current_year)))
            except Echeance.DoesNotExist:
                self.stdout.write('Pas de quittances impayées')
