from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')

app = Celery('Ecommerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
