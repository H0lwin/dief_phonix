from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserGroup

User = get_user_model()


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='تست',
            last_name='کاربر'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

    def test_user_str_representation(self):
        expected = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.user), expected)

    def test_get_display_name(self):
        display_name = self.user.get_display_name()
        expected = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(display_name, expected)


class UserGroupModelTests(TestCase):
    def setUp(self):
        self.group = UserGroup.objects.create(
            name='گروه تست',
            description='توضیحات گروه تست'
        )

    def test_create_group(self):
        self.assertEqual(self.group.name, 'گروه تست')
        self.assertEqual(self.group.description, 'توضیحات گروه تست')

    def test_group_str_representation(self):
        self.assertEqual(str(self.group), 'گروه تست')
