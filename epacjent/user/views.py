from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    context = {}
    return render(request, 'userPanel.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')
            context = {}
            return render(request, 'login.html', context)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userPanel')
        else:
            messages.error(request, 'Username or password valid')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')