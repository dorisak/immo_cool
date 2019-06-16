from django.contrib.auth.models import AnonymousUser, User, Permission, Group
from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from home.views import home, login_user, logout_view

# Test signup
class HomeTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@…',
            password='top_secret'
        )
        self.client = Client()
        #create permissions group
        group_name = "Gestionnaires"
        self.group = Group(name=group_name)
        self.group.save()

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

# test qu'un anonymous ne peut accéder à la homepage
    def test_anonymous_access_refused(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = home(request)
        self.assertEqual(response.status_code, 302)

#test login
    def test_login_response(self):
        # Get login page
        response = self.client.get('/login/')
        # Check response code
        self.assertEquals(response.status_code, 200)

#test permission login
    def test_user_cannot_access_home(self):
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_user_can_access_home(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

# test logout
    def test_logout_response(self):
        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 302)
