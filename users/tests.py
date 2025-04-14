from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.forms import CustomUserCreationForm


class CustomUserTests(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create(
            username='will',
            email='will@gmail.com',
            password='test123'
        )
        self.assertEqual('will', user.username)
        self.assertEqual('will@gmail.com', user.email)
        self.assertEqual('test123', user.password)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='wood',
            email='wood@gmail.com',
            password='test123'
        )
        self.assertEqual('wood', user.username)
        self.assertEqual('wood@gmail.com', user.email)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class SignupTests(TestCase):
    
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Signup')
        self.assertNotContains(self.response, 'Some dummy content')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)