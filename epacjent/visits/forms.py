from django.forms import ModelForm
from .models import Visit
from django import forms

class VisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'visit_hour': forms.TimeInput(attrs={'type': 'time'}),
        }