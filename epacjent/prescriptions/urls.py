from django.contrib import admin
from django.urls import path, include
from .views import index, generate_qr

urlpatterns = [
    path('', index, name='prescriptionsPanel'),
    path('qr/<str:data>', generate_qr, name='generate_qr')
]
