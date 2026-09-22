from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()

class AuthSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password123!',
            first_name='Test',
            last_name='User'
        )

    def test_login_and_dashboard(self):
        # 1. Login with valid credentials
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('dashboard'))

        # 2. Access dashboard
        dash_response = self.client.get(reverse('dashboard'))
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, 'testuser')

    def test_post_logout(self):
        self.client.login(username='testuser', password='Password123!')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_password_change(self):
        self.client.login(username='testuser', password='Password123!')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'Password123!',
            'new_password1': 'NewPassword456@',
            'new_password2': 'NewPassword456@',
        })
        self.assertRedirects(response, reverse('dashboard'))

        # Verify new password
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword456@'))

    def test_password_reset_flow(self):
        # Request password reset
        response = self.client.post(reverse('password_reset'), {
            'email': 'testuser@example.com'
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        # Check that one email has been created
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('password-reset-confirm', mail.outbox[0].body)

    def test_drf_api_info_endpoint(self):
        response = self.client.get(reverse('api_info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('framework', response.json())
        self.assertEqual(response.json()['status'], 'success')

