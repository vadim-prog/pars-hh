from .views import *
from django.urls import path

urlpatterns = [
     path('', SearchView.as_view(), name='home'),
     path('results/<int:pk>', ResultsView.as_view(), name='results'),
     path('about/', about, name='about'),
     path('contact/', contact, name='contact'),
]
