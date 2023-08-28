from django.contrib import admin
from django.urls import path, include
from visits.views import index, visit, createVisit, updateVisit

urlpatterns = [
    path('', index, name='visitsPanel'),
    path('<uuid:pk>', visit, name='visit'),
    path('create-visit', createVisit, name='create-visit'),
    path('update-visit/<uuid:pk>', updateVisit, name='update-visit')
]
