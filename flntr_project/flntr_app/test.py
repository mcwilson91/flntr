from django.test import TestCase
from flntr_app.models import StudentProfile, Landlord, Flat, Room
from django.contrib.auth import authenticate, login
from django.test.client import Client
from django.contrib.auth.models import User, Group, Permission


from django.core.urlresolvers import reverse


class IndexViewTests(TestCase):

    def test_index_view_with_no_flats(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no rooms available.")
        self.assertQuerysetEqual(response.context['recentflats'], [])

# the following 2 tests covers all views as they extend base
# which is the template containing the Navbar.
    def test_index_view_with_no_active_user(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")
        self.assertContains(response, "Log In")
        self.assertNotContains(response, "View My Profile")
        self.assertNotContains(response, "Manage Flats")
        self.assertNotContains(response, "Logout")
        self.assertNotContains(response, "Add Flat")

    def test_index_view_with_active_user(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")
        self.assertNotContains(response, "Register")
        self.assertNotContains(response, "Log In")
