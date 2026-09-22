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

