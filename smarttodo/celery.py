import os
from celery import Celery  # Stellen Sie sicher, dass Sie "pip install celery" ausgeführt haben

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarttodo.settings')
app = Celery('smarttodo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
