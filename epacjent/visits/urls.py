from django.urls import path
from visits.views import Index, VisitView, CreateVisitView, UpdateVisitView, CancelVisitView

app_name="visits"
urlpatterns = [
    path('', Index.as_view(), name='visitsPanel'),
    path('<uuid:pk>', VisitView.as_view(), name='visit'),
    path('create-visit', CreateVisitView.as_view(), name='create-visit'),
    path('update-visit/<uuid:pk>', UpdateVisitView.as_view(), name='update-visit'),
    path('cancel-visit/<uuid:pk>', CancelVisitView.as_view(), name='cancel-visit')
]
