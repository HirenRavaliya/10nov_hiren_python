from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def auth_home(request):
    return render(request, 'q13_auth/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('q13_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        pwd = request.POST.get('password', '')
        pwd2 = request.POST.get('confirm_password', '')
        if not username or not pwd:
            messages.error(request, 'Username and password are required.')
        elif pwd != pwd2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=pwd)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Account created! Welcome, {username}!')
            return redirect('q13_dashboard')
    return render(request, 'q13_auth/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('q13_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        pwd = request.POST.get('password', '')
        user = authenticate(request, username=username, password=pwd)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('q13_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'q13_auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('q13_login')

@login_required(login_url='/q13/login/')
def dashboard(request):
    return render(request, 'q13_auth/dashboard.html', {'user': request.user})

@login_required(login_url='/q13/login/')
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('q13_profile')

    return render(request, 'q13_auth/profile.html', {'user': request.user})