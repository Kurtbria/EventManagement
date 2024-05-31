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
        response = self.client.post(reverse('user_signup'), {
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
        self.assertRedirects(response, reverse('user_signup'))
        self.assertFalse(User.objects.filter(username='testuser').exists())


class GenerateTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_ticket(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/generate_ticket/', {'fullName': 'Test User', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket_template.html')
        self.assertEqual(response.context_data['full_name'], 'Test User')
        self.assertEqual(response.context_data['email'], 'test@example.com')
        self.assertTrue(response.context_data['ticket_number'])
        self.assertTrue(response.context_data['ticket_code'])


