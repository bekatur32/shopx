# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shopx.settings')

app = Celery('Shopx',backend='redis', broker="redis://localhost:6379/0")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

