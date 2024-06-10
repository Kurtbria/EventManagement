from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_signuo_post_success(self):
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
        self.assertTrue(User.objects.filter(username='testuser').exists())
