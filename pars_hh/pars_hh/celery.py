import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pars_hh.settings')

app = Celery('pars_hh')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
