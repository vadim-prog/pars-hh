from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddPostForm(forms.Form):
    vac_input = forms.CharField(max_length=255, label='Введите вакансию')  # Обычное поле для ввода
    reg_input = forms.CharField(max_length=255, label='Введите регион')
