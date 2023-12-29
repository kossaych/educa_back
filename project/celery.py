from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

# Configuration de Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charge automatiquement les tâches de Django depuis tous les modules "tasks.py"
app.autodiscover_tasks()
