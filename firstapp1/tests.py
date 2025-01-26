# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('login')

    def test_login_with_valid_credentials(self):
        # Test login with correct username and password
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Check if the response is a redirect (indicating a successful login)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_login_with_invalid_credentials(self):
        # Test login with incorrect password
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Check if the login page is reloaded with an error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_login_redirect_for_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        # Attempt to access the login page again
        response = self.client.get(self.login_url)
        # Check if the user is redirected (since they're already logged in)
        self.assertRedirects(response, '/')
