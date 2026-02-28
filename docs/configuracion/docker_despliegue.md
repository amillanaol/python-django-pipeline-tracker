# Despliegue con Docker

| Necesidad | Ubicacion |
| :--- | :--- |
| Levantar todo el stack | [Inicio Rapido](#inicio-rapido) |
| Servicios disponibles | [Servicios](#servicios) |
| Dockerfile multi-stage | [Dockerfile](#dockerfile) |
| Variables de entorno en Docker | [Variables de Entorno](#variables-de-entorno) |
| Persistencia de datos | [Volumenes](#volumenes) |

## Inicio Rapido

```bash
docker compose -f docker/docker-compose.yml up --build
```

La aplicacion estara disponible en `http://localhost:8000/api/`. El comando `web` ejecuta migraciones automaticamente antes de iniciar gunicorn.

## Servicios

Definidos en `docker/docker-compose.yml`:

| Servicio | Imagen | Puerto | Dependencias | Healthcheck |
| :--- | :--- | :--- | :--- | :--- |
| `web` | Build desde `docker/Dockerfile` | `8000:8000` | `db` (healthy), `redis` (started) | No |
| `db` | `postgres:16-alpine` | `5432:5432` | Ninguna | `pg_isready -U postgres` cada 5s |
| `redis` | `redis:7-alpine` | `6379:6379` | Ninguna | No |
| `celery` | Build desde `docker/Dockerfile` | Ninguno | `db` (healthy), `redis` (started) | No |

El servicio `web` ejecuta este comando de inicio:

```bash
python manage.py migrate --settings=src.infrastructure.django_app.settings.production &&
gunicorn src.infrastructure.django_app.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

El servicio `celery` ejecuta:

```bash
celery -A src.infrastructure.django_app.celery worker --loglevel=info
```

## Dockerfile

Archivo: `docker/Dockerfile`. Build multi-stage con Python 3.11-slim.

| Stage | Base | Proposito |
| :--- | :--- | :--- |
| `builder` | `python:3.11-slim` | Instala dependencias desde `pyproject.toml` |
| Final | `python:3.11-slim` | Copia site-packages y codigo fuente, ejecuta `collectstatic` |

El `collectstatic` se ejecuta con `|| true` para evitar fallos si no hay archivos estaticos configurados. El puerto expuesto es `8000`. El CMD por defecto es gunicorn con 3 workers.

## Variables de Entorno

Variables configuradas en `docker-compose.yml` para los servicios `web` y `celery`:

| Variable | Valor en Docker | Descripcion |
| :--- | :--- | :--- |
| `DJANGO_SETTINGS_MODULE` | `src.infrastructure.django_app.settings.production` | Modulo de settings |
| `DJANGO_SECRET_KEY` | `change-me-in-production` | Cambiar en produccion real |
| `DB_NAME` | `pipeline_tracker` | Nombre de la BD |
| `DB_USER` | `postgres` | Usuario de PostgreSQL |
| `DB_PASSWORD` | `postgres` | Contrasena de PostgreSQL |
| `DB_HOST` | `db` | Hostname del servicio PostgreSQL |
| `DB_PORT` | `5432` | Puerto de PostgreSQL |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Broker Redis |
| `CELERY_RESULT_BACKEND` | `redis://redis:6379/0` | Backend de resultados Redis |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts permitidos |

Variables del servicio `db`:

| Variable | Valor | Descripcion |
| :--- | :--- | :--- |
| `POSTGRES_DB` | `pipeline_tracker` | Base de datos a crear |
| `POSTGRES_USER` | `postgres` | Usuario PostgreSQL |
| `POSTGRES_PASSWORD` | `postgres` | Contrasena PostgreSQL |

## Volumenes

| Volumen | Servicio | Mount Point | Proposito |
| :--- | :--- | :--- | :--- |
| `postgres_data` | `db` | `/var/lib/postgresql/data` | Persistencia de datos PostgreSQL |

## Resolucion de Errores

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| `web` se reinicia en bucle | `db` no esta healthy todavia | Verificar que el healthcheck de `db` pasa con `docker compose ps` |
| `connection refused` a PostgreSQL | `DB_HOST` incorrecto | Debe ser `db` (nombre del servicio), no `localhost` |
| `celery` no procesa tareas | Redis no disponible | Verificar que el servicio `redis` esta corriendo |
| `collectstatic` falla en build | Falta configuracion de staticfiles | El `|| true` lo maneja; no bloquea el build |

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
