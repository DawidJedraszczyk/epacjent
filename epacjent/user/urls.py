from django.contrib import admin
from django.urls import path, include
from user.views import index, login_user, logout_user

app_name='user'
urlpatterns = [
    path('', index, name='userPanel'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
