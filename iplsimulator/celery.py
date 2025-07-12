import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iplsimulator.settings")

from django.conf import settings

app = Celery("settings", broker="redis://localhost:6379/0")

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

app.config_from_object("django.conf:settings")
app.autodiscover_tasks()