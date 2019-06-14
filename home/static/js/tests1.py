from django.test import TestCase
from products.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

# Test signup
class RegisterTest(TestCase):

    def setUp(self):
        self.password_creation = User.objects.create(email="test@testeste.com", password="Blabliblo2")

    def test_uses_signup_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        self.test_password = False
        self.logging = authenticate(email="test@testeste.com", password="Blabliblo2")
        if self.logging:
            response = self.client.get(self.logging)
            self.test_password = True
            self.assertEqual(response['password'], "Blabliblo2")
