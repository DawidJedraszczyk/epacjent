from django.contrib import admin
from django.urls import path, include
from .views import Index, Generate_qr

app_name='prescriptions'
urlpatterns = [
    path('', Index.as_view(), name='prescriptionsPanel'),
    path('qr/<str:data>', Generate_qr.as_view(), name='generate_qr')
]
