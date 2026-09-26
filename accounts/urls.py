from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

# DRF Router
router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('tasks', views.TaskViewSet, basename='task')


urlpatterns = [
    # Home & Dashboard
    path('', views.dashboard_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # REST API Endpoints
    path('api/', views.api_info_view, name='api_info'),
    path('api/users/', views.UserListAPIView.as_view(), name='api_user_list'),
    path('api/v1/', include(router.urls)),
    path('api/v1/task-stats/', views.task_statistics_view, name='task_stats'),

    # Password Change (Logged in)
    path('password-change/', views.change_password_view, name='password_change'),

    # Password Reset (Forgotten password flow)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            form_class=CustomPasswordResetForm,
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            form_class=CustomSetPasswordForm
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
