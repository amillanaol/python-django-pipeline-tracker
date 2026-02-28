import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    load_dotenv(env_path, override=False)

from celery import Celery  # noqa: E402

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.infrastructure.django_app.settings.production",
)

app = Celery("pipeline_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["src.infrastructure.tasks"])
