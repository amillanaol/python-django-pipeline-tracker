import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.infrastructure.django_app.settings.production",
)

app = Celery("pipeline_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["src.infrastructure.tasks"])
