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
        city = self.cleaned_data['city']
        req = requests.get('https://api.hh.ru/suggests/areas', {'text': city})
        data = req.content
        req.close()
        jsobj = json.loads(data)
        try:
            jsobj["items"][0]["id"]
        except IndexError:
            raise ValidationError('Введите корректный город')
        return city
