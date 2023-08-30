from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View


class Index(View):
    template_name = "userPanel.html"
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

class Login_user(View):
    template_name = 'login.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            context = {}
            return render(request, self.template_name, context)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:userPanel')
        else:
            messages.error(request, 'Invalid username or password')

        context = {}
        return render(request, self.template_name, context)

class Logout_user(View):
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        logout(request)
        return redirect('user:login')