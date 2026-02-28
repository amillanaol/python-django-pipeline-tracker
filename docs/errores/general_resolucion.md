# Resolucion de Errores

| Necesidad | Ubicacion |
| :--- | :--- |
| Errores de instalacion y dependencias | [Errores Comunes](#errores-comunes) |
| Errores de base de datos | [Errores de Base de Datos](#errores-de-base-de-datos) |
| Errores de configuracion | [Errores de Configuracion](#errores-de-configuracion) |

Errores comunes que pueden presentarse durante el desarrollo y despliegue del proyecto Pipeline Tracker.

## Errores Comunes

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| pip install se congela con backtracking | Conflicto de versiones entre dependencias | Verificar requires-python coincide con python --version; usar constraints exactos en pyproject.toml |
| ModuleNotFoundError: src.infrastructure | Paquete no instalado en modo editable | Ejecutar pip install -e . desde la raiz del proyecto |
| OperationalError: no such table: pipeline_runs | Migraciones no aplicadas | python manage.py makemigrations && python manage.py migrate |
| django.db.utils.OperationalError | PostgreSQL no disponible | Usar development.py (SQLite) o levantar docker compose up db |
| Tests de integracion fallan sin DB | DJANGO_SETTINGS_MODULE no apunta a settings con DB | Exportar DJANGO_SETTINGS_MODULE=src.infrastructure.django_app.settings.development |
| Celery no descubre tareas | Modulo de tareas no registrado | Verificar autodiscover_tasks en celery.py |
| Puerto 8000 ya en uso | Puerto ocupado por otro proceso | Cambiar puerto en .env: PORT=8181, o ejecutar kill en proceso |
| Puerto 8181 no funciona | Puerto no configurado correctamente | Verificar que el archivo .env existe y contiene PORT=8181; recrear archivo si es necesario |

## Errores de Base de Datos

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| django.db.utils.OperationalError: could not connect to server | PostgreSQL no esta ejecutandose | Verificar que PostgreSQL esta corriendo: docker compose up -d db |
| Peer authentication failed for user postgres | Metodo de autenticacion incorrecto en PostgreSQL | Modificar pg_hba.conf o usar autenticacion por password |
| database is locked | SQLite con multiples conexiones simultaneas | Usar PostgreSQL en produccion o cerrar otras conexiones |

## Errores de Configuracion

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| ModuleNotFoundError: No module named 'dotenv' | Dependencia python-dotenv no instalada | pip install python-dotenv |
| DEBUG=False pero ALLOWED_HOSTS vacio | Configuracion de produccion incompleta | Agregar dominios a ALLOWED_HOSTS en .env |
| CORS error en navegador | CORS no configurado correctamente | Verificar CORS_ALLOWED_ORIGINS en settings |

## Control de versiones

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol(https://orcid.org/0009-0003-1768-7048) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-28 |
