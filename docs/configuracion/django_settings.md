# Configuracion Django

| Necesidad | Ubicacion |
| :--- | :--- |
| Variables de entorno requeridas | [Variables de Entorno](#variables-de-entorno) |
| Diferencias entre entornos | [Comparativa de Entornos](#comparativa-de-entornos) |
| Apps instaladas | [INSTALLED_APPS](#installed-apps) |
| Configuracion de Celery | [Celery](#celery) |

## Archivos de Settings

| Archivo | Proposito | Variable `DJANGO_SETTINGS_MODULE` |
| :--- | :--- | :--- |
| `src/infrastructure/django_app/settings/base.py` | Configuracion compartida | No se usa directamente |
| `src/infrastructure/django_app/settings/development.py` | Desarrollo local | `src.infrastructure.django_app.settings.development` |
| `src/infrastructure/django_app/settings/production.py` | Produccion / Docker | `src.infrastructure.django_app.settings.production` |

`manage.py` apunta por defecto a `development`. `wsgi.py` y `celery.py` apuntan por defecto a `production`.

## Comparativa de Entornos

| Parametro | Development | Production |
| :--- | :--- | :--- |
| `DEBUG` | `True` | `False` |
| Database Engine | SQLite (`db.sqlite3`) | PostgreSQL |
| `ALLOWED_HOSTS` | `["*"]` | Desde env `ALLOWED_HOSTS` (comma-separated) |
| CORS | `CORS_ALLOW_ALL_ORIGINS = True` | `CORS_ALLOWED_ORIGINS` desde env |
| `SECURE_SSL_REDIRECT` | No configurado | Desde env (default `True`) |
| `SESSION_COOKIE_SECURE` | No configurado | `True` |
| `CSRF_COOKIE_SECURE` | No configurado | `True` |
| HSTS | No configurado | 1 ano, include subdomains, preload |

## Variables de Entorno

| Variable | Default | Entorno | Descripcion |
| :--- | :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | `django-insecure-dev-only-...` | base | Clave secreta Django |
| `DB_NAME` | `pipeline_tracker` | production | Nombre de la base de datos PostgreSQL |
| `DB_USER` | `postgres` | production | Usuario de la base de datos |
| `DB_PASSWORD` | `postgres` | production | Contrasena de la base de datos |
| `DB_HOST` | `localhost` | production | Host de la base de datos |
| `DB_PORT` | `5432` | production | Puerto de la base de datos |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | base | URL del broker Celery (Redis) |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | base | URL del backend de resultados |
| `ALLOWED_HOSTS` | `""` | production | Hosts permitidos (comma-separated) |
| `CORS_ALLOWED_ORIGINS` | `""` | production | Origenes CORS permitidos (comma-separated) |
| `SECURE_SSL_REDIRECT` | `"True"` | production | Redirigir HTTP a HTTPS |

## INSTALLED_APPS

Definido en `src/infrastructure/django_app/settings/base.py:15`:

| App | Tipo | Proposito |
| :--- | :--- | :--- |
| `django.contrib.admin` | Django | Panel de administracion |
| `django.contrib.auth` | Django | Autenticacion |
| `django.contrib.contenttypes` | Django | Content types framework |
| `django.contrib.sessions` | Django | Sesiones |
| `django.contrib.messages` | Django | Sistema de mensajes |
| `django.contrib.staticfiles` | Django | Archivos estaticos |
| `rest_framework` | Terceros | Django REST Framework |
| `corsheaders` | Terceros | CORS headers |
| `django_filters` | Terceros | Filtrado en DRF |
| `src.infrastructure.persistence` | Local | Modelos ORM del proyecto |

## Middleware

Orden definido en `base.py:30`:

| Posicion | Middleware | Proposito |
| :--- | :--- | :--- |
| 1 | `SecurityMiddleware` | Headers de seguridad |
| 2 | `WhiteNoiseMiddleware` | Servir archivos estaticos |
| 3 | `CorsMiddleware` | CORS |
| 4 | `SessionMiddleware` | Sesiones |
| 5 | `CommonMiddleware` | Middleware comun |
| 6 | `CsrfViewMiddleware` | Proteccion CSRF |
| 7 | `AuthenticationMiddleware` | Autenticacion |
| 8 | `MessageMiddleware` | Mensajes |
| 9 | `XFrameOptionsMiddleware` | Clickjacking |

## Celery

Configuracion en `src/infrastructure/django_app/celery.py` y parametros en `base.py:105`.

| Parametro | Valor | Archivo |
| :--- | :--- | :--- |
| App name | `pipeline_tracker` | `celery.py:10` |
| Config source | `django.conf:settings` (namespace `CELERY`) | `celery.py:11` |
| Autodiscover | `["src.infrastructure.tasks"]` | `celery.py:12` |
| `ACCEPT_CONTENT` | `["json"]` | `base.py:107` |
| `TASK_SERIALIZER` | `json` | `base.py:108` |
| `RESULT_SERIALIZER` | `json` | `base.py:109` |

## Archivos Estaticos

| Parametro | Valor |
| :--- | :--- |
| `STATIC_URL` | `static/` |
| `STATIC_ROOT` | `{BASE_DIR}/staticfiles` |
| Storage backend | `whitenoise.storage.CompressedManifestStaticFilesStorage` |

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
