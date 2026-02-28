FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN DJANGO_SETTINGS_MODULE=src.infrastructure.django_app.settings.production \
    python manage.py collectstatic --noinput 2>/dev/null || true

ENV PORT=8181

EXPOSE ${PORT}

CMD gunicorn src.infrastructure.django_app.wsgi:application --bind 0.0.0.0:${PORT} --workers 3
