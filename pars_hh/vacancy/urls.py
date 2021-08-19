from .views import *
from django.urls import path

urlpatterns = [
     path('', index, name='home'),
     path('results/', results, name='results'),
     path('about/', about, name='about'),
     path('contact/', contact, name='contact'),  # Устанавливаем маршруты между ссылкой и представлением
]
