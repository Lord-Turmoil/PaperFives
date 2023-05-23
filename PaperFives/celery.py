"""
WSGI config for PaperFives project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://realpython.com/asynchronous-tasks-with-django-and-celery/#why-use-celery
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PaperFives.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
