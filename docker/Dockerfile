FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN python manage.py collectstatic --noinput --settings=src.infrastructure.django_app.settings.production 2>/dev/null || true

EXPOSE 8000

CMD ["gunicorn", "src.infrastructure.django_app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
