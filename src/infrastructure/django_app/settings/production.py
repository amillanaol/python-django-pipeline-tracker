import os
from urllib.parse import urlparse

from .base import *  # noqa: F401, F403

DEBUG = os.environ.get("DEBUG", "False") == "True"

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    DATABASES = {  # noqa: F405
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "postgres",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "localhost",
            "PORT": str(parsed.port or 5432),
        }
    }

ALLOWED_HOSTS = [
    host for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host
]

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
CSRF_COOKIE_SECURE = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CORS_ALLOWED_ORIGINS = [
    origin for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if origin
]
