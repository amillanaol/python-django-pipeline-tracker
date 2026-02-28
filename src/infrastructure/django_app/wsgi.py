import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    load_dotenv(env_path)

from django.core.wsgi import get_wsgi_application  # noqa: E402

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.infrastructure.django_app.settings.production",
)

application = get_wsgi_application()
