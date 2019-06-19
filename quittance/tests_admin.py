from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from .models import Echeance, Quittance
from rental.models import Rental, Property, Bedroom
from home.models import Administrator
from occupant.models import Occupant
from .admin import EcheanceAdminModel
from datetime import date


class MockRequest(object):
    pass

request = MockRequest()


class EcheanceModelAdminTest(TestCase):
    """ Test for echeance sending through modeladmin action """

    def setUp(self):
        today = date.today()
        self.echeance_admin = EcheanceAdminModel(Echeance, AdminSite())
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@…',
            password='top_secret'
            )
        self.user_2 = User.objects.create_user(
            username='aline',
            email='alineb@…',
            password='top_secret2'
            )
        self.occupant_test = Occupant.objects.create(
            user = self.user,
            is_active =True,
            date_of_entry = today,
            date_of_leaving = today,
            last_update = today,
            creation_date = today,
            deposit =  300,
            suivi = 'blabla',
        )
        self.admin_test = Administrator.objects.create(
            user = self.user_2,
            address = '13 rue de soulino, 75019 Paris'
        )
        self.property_test = Property.objects.create(
            name = 'Propriété Renaud',
            address= '16 rue de pikouli, 75019 Paris',
            number_of_bedroom = 3,
            superficy = 80,
            administrator = self.admin_test,
        )
        self.bedroom_test = Bedroom.objects.create(
            name = 'Chambre 1',
            occupency = True,
            superficy = 10,
            property = self.property_test,
        )
        self.rental_test = Rental.objects.create(
            occupant = self.occupant_test,
            bedroom = self.bedroom_test,
            rent_amount = 230,
            charges = 0,
            property = self.property_test,
            archived = False,
        )

    def test_bulk_rent_paid(self):
        today = date.today()
        app1 = Echeance.objects.create(echeance='{}-{}.pdf'.format(today, self.user),
            monthly_rent_paid=False,
            date_of_issue= today,
            rental=self.rental_test
        )
        queryset = Echeance.objects.filter(pk=app1.pk)
        self.echeance_admin.bulk_rent_paid(request, queryset)
        self.assertTrue(Echeance.objects.get(pk=app1.pk).monthly_rent_paid)


    def test_bulk_rent_unpaid(self):
        today = date.today()
        app1 = Echeance.objects.create(echeance='{}-{}.pdf'.format(today, self.user),
            monthly_rent_paid=True,
            date_of_issue= today,
            rental=self.rental_test
        )
        queryset = Echeance.objects.filter(pk=app1.pk)
        self.echeance_admin.bulk_rent_unpaid(request, queryset)
        self.assertFalse(Echeance.objects.get(pk=app1.pk).monthly_rent_paid)
