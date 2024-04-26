from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import generate_ticket 

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_post_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertRedirects(response, reverse('signin'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_post_missing_fields(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_post_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'mismatchpassword'
        })
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_post_existing_username(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='existingpassword')
        response = self.client.post(reverse('signup'), {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(email='test@example.com').exists())

    def test_signup_post_existing_email(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='existingpassword')
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'existing@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(username='testuser').exists())


class GenerateTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_ticket(self):
        # Create a user for the test
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a POST request to the view
        response = self.client.post('/generate_ticket/', {'fullName': 'Test User', 'email': 'test@example.com'})

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'ticket_template.html')

        # Check if the context data contains the expected values
        self.assertEqual(response.context_data['full_name'], 'Test User')
        self.assertEqual(response.context_data['email'], 'test@example.com')
        self.assertTrue(response.context_data['ticket_number'])
        self.assertTrue(response.context_data['ticket_code'])
