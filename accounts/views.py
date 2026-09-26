from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserRegistrationForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm
)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('login')
    # If GET request, redirect safely back to dashboard
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html", {"user": request.user})


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_info_view(request):
    return Response({
        "status": "success",
        "message": "Welcome to Django REST Framework API!",
        "framework": "Django REST Framework 3.18.3",
        "endpoints": {
            "api_info": "/api/",
            "api_users": "/api/users/",
            "api_auth_login": "/api-auth/login/",
            "api_auth_logout": "/api-auth/logout/",
        }
    })


from rest_framework import generics, permissions
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserListAPIView(generics.ListAPIView):
    """
    API endpoint that returns user list using DRF Generic Views and ModelSerializer
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


from rest_framework import viewsets
from rest_framework.decorators import action

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet that provides 'list' and 'retrieve' actions for users,
    plus a custom action 'me' to get the current authenticated user's profile.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD API for Tasks:
    - GET    /api/v1/tasks/       -> list tasks
    - POST   /api/v1/tasks/       -> create task
    - GET    /api/v1/tasks/{id}/  -> retrieve task
    - PUT    /api/v1/tasks/{id}/  -> update task
    - PATCH  /api/v1/tasks/{id}/  -> partial update task
    - DELETE /api/v1/tasks/{id}/  -> delete task
    - POST   /api/v1/tasks/{id}/toggle/ -> custom action to toggle completion status
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user).order_by('-created_at')
        return Task.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle(self, request, pk=None):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return Response({
            "status": "success",
            "task_id": task.id,
            "is_completed": task.is_completed,
            "message": "Task completion status toggled successfully."
        }, status=status.HTTP_200_OK)


from rest_framework.decorators import permission_classes

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_statistics_view(request):
    """
    Function-Based API View (FBV) that returns aggregated task statistics
    for the authenticated user.
    """
    user_tasks = Task.objects.filter(user=request.user)
    total = user_tasks.count()
    completed = user_tasks.filter(is_completed=True).count()
    pending = total - completed
    rate = f"{(completed / total * 100):.1f}%" if total > 0 else "0%"

    return Response({
        "status": "success",
        "user": request.user.username,
        "statistics": {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_rate": rate,
        }
    })



