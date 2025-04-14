from django.contrib.auth import get_user_model
from django.test import TestCase


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


