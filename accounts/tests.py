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

    def test_drf_user_list_endpoint(self):
        response = self.client.get(reverse('api_user_list'))
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertIsInstance(users, list)
        self.assertTrue(len(users) >= 1)
        # Check ModelSerializer fields and SerializerMethodField
        self.assertEqual(users[0]['username'], 'testuser')
        self.assertIn('full_name', users[0])

    def test_viewset_and_router(self):
        # 1. Router list action (user-list)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)

        # 2. Router retrieve action (user-detail)
        response_detail = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response_detail.status_code, 200)
        self.assertEqual(response_detail.json()['username'], 'testuser')

        # 3. Custom action 'me' without authentication
        response_me_anon = self.client.get(reverse('user-me'))
        self.assertIn(response_me_anon.status_code, [401, 403])

        # 4. Custom action 'me' with authentication
        self.client.login(username='testuser', password='Password123!')
        response_me = self.client.get(reverse('user-me'))
        self.assertEqual(response_me.status_code, 200)
        self.assertEqual(response_me.json()['username'], 'testuser')

    def test_task_crud_lifecycle(self):
        self.client.login(username='testuser', password='Password123!')

        # 1. CREATE (POST) -> 201 Created
        post_response = self.client.post(
            reverse('task-list'),
            data={'title': 'Learn Django REST Framework CRUD', 'description': 'Complete the lesson and test'},
            content_type='application/json'
        )
        self.assertEqual(post_response.status_code, 201)
        task_data = post_response.json()
        task_id = task_data['id']
        self.assertEqual(task_data['title'], 'Learn Django REST Framework CRUD')
        self.assertEqual(task_data['is_completed'], False)

        # 2. READ LIST (GET) -> 200 OK
        list_response = self.client.get(reverse('task-list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(len(list_response.json()) >= 1)

        # 3. READ DETAIL (GET) -> 200 OK
        detail_response = self.client.get(reverse('task-detail', kwargs={'pk': task_id}))
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()['id'], task_id)

        # 4. UPDATE (PATCH) -> 200 OK
        patch_response = self.client.patch(
            reverse('task-detail', kwargs={'pk': task_id}),
            data={'description': 'Updated description!'},
            content_type='application/json'
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()['description'], 'Updated description!')

        # 5. CUSTOM ACTION TOGGLE (POST) -> 200 OK
        toggle_response = self.client.post(reverse('task-toggle', kwargs={'pk': task_id}))
        self.assertEqual(toggle_response.status_code, 200)
        self.assertEqual(toggle_response.json()['is_completed'], True)

        # 6. DELETE (DELETE) -> 204 No Content
        delete_response = self.client.delete(reverse('task-detail', kwargs={'pk': task_id}))
        self.assertEqual(delete_response.status_code, 204)

        # 7. VERIFY DELETED -> 404 Not Found
        get_deleted = self.client.get(reverse('task-detail', kwargs={'pk': task_id}))
        self.assertEqual(get_deleted.status_code, 404)

    def test_task_statistics_fbv(self):
        # 1. Unauthenticated request rejected
        anon_response = self.client.get(reverse('task_stats'))
        self.assertIn(anon_response.status_code, [401, 403])

        # 2. Authenticated request
        self.client.login(username='testuser', password='Password123!')
        from .models import Task
        Task.objects.create(user=self.user, title='Test Task 1', is_completed=True)
        Task.objects.create(user=self.user, title='Test Task 2', is_completed=False)

        auth_response = self.client.get(reverse('task_stats'))
        self.assertEqual(auth_response.status_code, 200)
        data = auth_response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['statistics']['total_tasks'], 2)
        self.assertEqual(data['statistics']['completed_tasks'], 1)
        self.assertEqual(data['statistics']['pending_tasks'], 1)
        self.assertEqual(data['statistics']['completion_rate'], '50.0%')

    def test_jwt_authentication_flow(self):
        # 1. Obtain JWT token pair (POST /api/token/)
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            data={'username': 'testuser', 'password': 'Password123!'},
            content_type='application/json'
        )
        self.assertEqual(token_response.status_code, 200)
        tokens = token_response.json()
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)

        access_token = tokens['access']
        refresh_token = tokens['refresh']

        # 2. Access protected endpoint with Bearer token
        protected_response = self.client.get(
            reverse('task_stats'),
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        self.assertEqual(protected_response.status_code, 200)
        self.assertEqual(protected_response.json()['user'], 'testuser')

        # 3. Verify access token (/api/token/verify/)
        verify_response = self.client.post(
            reverse('token_verify'),
            data={'token': access_token},
            content_type='application/json'
        )
        self.assertEqual(verify_response.status_code, 200)

        # 4. Refresh token to get new access token (/api/token/refresh/)
        refresh_response = self.client.post(
            reverse('token_refresh'),
            data={'refresh': refresh_token},
            content_type='application/json'
        )
        self.assertEqual(refresh_response.status_code, 200)
        new_tokens = refresh_response.json()
        self.assertIn('access', new_tokens)






