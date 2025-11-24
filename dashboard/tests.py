from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import DashboardWidget

User = get_user_model()


class DashboardViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_dashboard_accessible_to_logged_in_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_stats_endpoint(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/stats/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_users', data)
        self.assertIn('total_groups', data)


class DashboardWidgetModelTests(TestCase):
    def setUp(self):
        self.widget = DashboardWidget.objects.create(
            title='ویجت تست',
            description='توضیحات ویجت',
            widget_type='stats',
            is_active=True
        )

    def test_create_widget(self):
        self.assertEqual(self.widget.title, 'ویجت تست')
        self.assertEqual(self.widget.widget_type, 'stats')
        self.assertTrue(self.widget.is_active)

    def test_widget_str_representation(self):
        self.assertEqual(str(self.widget), 'ویجت تست')
