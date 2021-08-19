from django.db import models
from django.urls import reverse

'''
class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
    '''
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
    address = models.CharField(max_length=50, blank=True, verbose_name="Адрес")  # blank=True - поле может быть и пустям, по у молчанию False
    url_link = models.URLField(verbose_name="Ссылка на вакансию")
    input_vac = models.ForeignKey(Search, on_delete=models.CASCADE, verbose_name="ForeignKey")
