from django.contrib import admin
from django.urls import path, include
from user.views import Index, Logout_user, Login_user

app_name='user'
urlpatterns = [
    path('', Index.as_view(), name='userPanel'),
    path('login/', Login_user.as_view(), name='login'),
    path('logout/', Logout_user.as_view(), name='logout'),
]
