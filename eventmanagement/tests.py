from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from .utils import send_welcome_email

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_signup_post_success(self):
        response = self.client.post(reverse('user_signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_post_missing_fields(self):
        response = self.client.post(reverse('user_signup'), {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_post_password_mismatch(self):
        response = self.client.post(reverse('user_signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'mismatchpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='testuse').exists())

    def test_signup_post_existing_username(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='existingpassword')
        response = self.client.post(reverse('user_signup'), {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='testuser').exists())
    

    def test_signup_post_existing_email(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='existingpassword')
        response = self.client.post(reverse('user_signup'), {
            'username': 'testuser',
            'email': 'existing@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'success': False, 'error_message': 'Email is already registered'}
        )
        self.assertFalse(User.objects.filter(username='testuser').exists())

class GenerateTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpasword')


    def test_generate_ticket(self):

        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('generate_ticket'), {
            'fullname': 'Test User',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket_template.html')
        self.assertEqual(response.context['full_name'], 'Test User')
        self.assertEqual(response.context['email'], 'test@example.com')
        self.assertTrue(response.context['ticket_number'])
        self.assertTrue(response.context['ticket_code'])

class EmailTestCase(TestCase):
    def test_welcome_email_sent(self):
        send_welcome_email('#')

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject, 'Welcome to EMS!!')
        self.assertInHTML('<h1>Welcome to EMS!!<h1>', mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].from_email, '#')
        self.assertEqual(mail.outbox[0].to[0], '#')
