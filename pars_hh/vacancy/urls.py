from .views import *
from django.urls import path, re_path

urlpatterns = [
     #path('', index, name='home'),
     path('', SearchView.as_view(), name='home'),
     #path('results/', about, name='results'),
     path('results/<int:pk>', ResultsView.as_view(), name='results'),
     #path('results/', ResultsView.as_view(), name='results'),
     path('about/', about, name='about'),
     path('contact/', contact, name='contact'),  # Устанавливаем маршруты между ссылкой и представлением
]
