from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('visits/', include('visits.urls')),
    path('prescriptions/', include('prescriptions.urls')),
]
