from django.db import models
from django.urls import reverse


class Search(models.Model):
    input_vacancy = models.CharField(max_length=50, verbose_name="Запрос вакансии")
    city = models.CharField(max_length=20, verbose_name="Регион")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время запроса")

class Output_data(models.Model):  # Результаты поиска
    vacancy = models.CharField(max_length=50, verbose_name="Вакансия")
    description = models.CharField(max_length=1000, verbose_name="Описание")
    salary = models.CharField(max_length=20, blank=True, verbose_name="Зарплата")
    skills = models.CharField(max_length=255, blank=True, verbose_name="Навыки")
    company = models.CharField(max_length=50, verbose_name="Компания")
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name="Адрес")  # blank=True - поле может быть и пустям, по у молчанию False
    url_link = models.URLField(verbose_name="Ссылка на вакансию")
    input_vac = models.ForeignKey(Search, on_delete=models.CASCADE, verbose_name="ForeignKey")
