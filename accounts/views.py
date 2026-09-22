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
