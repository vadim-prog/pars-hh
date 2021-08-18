from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from pars_hh import settings
from vacancy.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancy.urls')),  # Подключаем маршруты из приложения
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
