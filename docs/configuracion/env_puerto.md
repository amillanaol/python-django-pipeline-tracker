| Necesidad | Ubicación |
| :--- | :--- |
| Configurar variables de entorno | `.env` |
| Cambiar puerto del servidor | `.env` (variable `PORT`) |
| Ver configuración de Django | `src/infrastructure/django_app/settings/base.py` |

## Cargar Variables de Entorno

El proyecto utiliza `python-dotenv` para cargar variables desde un archivo `.env`.

| Archivo | Propósito |
| :--- | :--- |
| `.env` | Variables locales (NO versionar) |
| `.env.example` | Plantilla con valores por defecto |

## Puerto del Servidor

| Variable | Valor por Defecto | Descripción |
| :--- | :--- | :--- |
| `PORT` | `8000` | Puerto donde corre Django |

### Cambiar Puerto

1. Editar archivo `.env` en la raíz del proyecto:
   ```
   PORT=8181
   ```

2. Levantar servidor:
   ```bash
   python manage.py runserver
   ```

El puerto se aplica automáticamente desde `.env` via `manage.py`.

## Archivo `.env.example`

```bash
# Django
DJANGO_SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
PORT=8181

# Database (PostgreSQL)
DB_NAME=pipeline_tracker
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Otras Variables de Entorno

| Variable | Default | Sección |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | `django-insecure-dev-only-change-in-production` | Django |
| `DEBUG` | `False` | Django |
| `ALLOWED_HOSTS` | vacío | Django |
| `DB_NAME` | `pipeline_tracker` | Database |
| `DB_USER` | `postgres` | Database |
| `DB_PASSWORD` | `postgres` | Database |
| `DB_HOST` | `localhost` | Database |
| `DB_PORT` | `5432` | Database |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | Celery |

## Desarrollo Inicial

```bash
# 1. Copiar plantilla
cp .env.example .env

# 2. Editar puerto si es necesario
# PORT=8181

# 3. Instalar dependencias
pip install -e .

# 4. Crear migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Levantar servidor
python manage.py runserver
```

## Control de versiones

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol(https://orcid.org/0009-0003-1768-7048) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
