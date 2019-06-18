import tempfile
import os
from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core import mail
from django.core.mail import outbox
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from datetime import datetime, date
from quittance.models import Quittance
from home.models import Administrator
from rental.models import Property, Bedroom, Rental
from occupant.models import Occupant
from quittance.models import Quittance


#select only late people
class PdfCreationTest(TestCase):

    def setUp(self):
        self.day = date.today()
        self.current_month = self.day.month
        self.current_year = self.day.year
        self.user1 = User(
            username='jacob',
            email='jacob@…',
            password='top_secret'
            )
        self.user2 = User(
            username='antoine',
            email='anto@…',
            password='top_secretbis'
            )
        self.user3 = User(
            username='Romaine',
            email='roro@…',
            password='top_secretter'
            )
        User.objects.bulk_create([self.user1, self.user2, self.user3])

        self.admin = Administrator.objects.create(
            user = self.user3,
            address = '13 rue de soulino, 75019 Paris'
        )

        self.property_test = Property.objects.create(
            name = 'Propriété Renaud',
            address= '16 rue de pikouli, 75019 Paris',
            number_of_bedroom = 3,
            superficy = 80,
            administrator = self.admin,
        )

        self.bedroom1 = Bedroom(
            name = 'Chambre 1',
            occupency = True,
            superficy = 10,
            property = self.property_test,
        )
        self.bedroom2 = Bedroom(
            name = 'Chambre 2',
            occupency = True,
            superficy = 10,
            property = self.property_test,
        )
        Bedroom.objects.bulk_create([self.bedroom1, self.bedroom2])

        self.occupant1 = Occupant(
            user = self.user1,
            is_active =True,
            date_of_entry = self.day,
            date_of_leaving = self.day,
            last_update = self.day,
            creation_date = self.day,
            deposit =  300,
            suivi = 'blabla',
        )
        self.occupant2 = Occupant(
            user = self.user2,
            is_active =True,
            date_of_entry = self.day,
            date_of_leaving = self.day,
            last_update = self.day,
            creation_date = self.day,
            deposit =  300,
            suivi = 'blablatest',
        )
        Occupant.objects.bulk_create([self.occupant1, self.occupant2])

        self.rental1 = Rental(
            occupant = self.occupant1,
            bedroom = self.bedroom1,
            rent_amount = 230,
            charges = 0,
            property = self.property_test,
            archived = False,
        )
        self.rental2 = Rental(
            occupant = self.occupant2,
            bedroom = self.bedroom2,
            rent_amount = 230,
            charges = 0,
            property = self.property_test,
            archived = False,
        )
        Rental.objects.bulk_create([self.rental1, self.rental2])

        # self.record1 = Quittance.objects.create(quittance='{}-{}.pdf'.format(self.day, self.user1),
        #     monthly_rent_paid=False,
        #     date_of_issue=self.day,
        #     rental=self.rental1
        # )
        # self.record2 = Quittance(quittance='{}-{}.pdf'.format(self.day, self.user2), monthly_rent_paid=True, date_of_issue=self.day, rental=self.rental2)
        # self.bulk_creation = Quittance.objects.bulk_create([self.record1, self.record2,])

    def teardown(self):
        os.remove(self.bulk_creation)

    # check message for quittance sent
    def test_message_sent(self):
        out = StringIO()
        call_command('pdf_creation', stdout=out)
        self.assertIn("Le mail pour {} a bien été envoyé".format(self.rental1.occupant), out.getvalue())


    #verify mail sent to the occupant
    def test_mail_sent(self):
        mail.send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com', [self.user1.email],
            fail_silently=False
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


    #verify pdf creation and saving
    # @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    # def test_pdf_creation(self):
    #     temp_file = tempfile.NamedTemporaryFile()
    #     test_pdf = self.record1
    #     self.assertEqual(len(Quittance.objects.all()), 1)
