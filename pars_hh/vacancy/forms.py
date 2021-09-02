from django import forms
from .models import *
from django.core.exceptions import ValidationError
import requests
import json


class AddSearchForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
    '''

    class Meta:
        model = Search
        fields = ['input_vacancy', 'city']
        widgets = {
            'input_vacancy': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'})
        }

    def clean_city(self):
        city = self.cleaned_data('city')
        if city is not 'Омск':
            raise ValidationError('Введите корректный город')
        return city
