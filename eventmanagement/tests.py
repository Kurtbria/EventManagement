from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

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


class GenerateTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_ticket(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/generate_ticket/', {'fullname': 'Test User', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket_template.html')
        self.assertEqual(response.context['full_name'], 'Test User')
        self.assertEqual(response.context['email'], 'test@example.com')
        self.assertTrue(response.context['ticket_number'])
        self.assertTrue(response.context['ticket_code'])