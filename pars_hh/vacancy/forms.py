from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddSearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['input_vacancy', 'city']
        widgets = {
            'input_vacancy': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'})
        }
