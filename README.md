# Pipeline Tracker — DevSecOps Dashboard

| Necesidad | Ubicacion |
| :--- | :--- |
| Instalar y ejecutar localmente | [docs/desarrollo/instalacion_local.md](docs/desarrollo/instalacion_local.md) |
| Entender la arquitectura DDD Hexagonal | [docs/arquitectura/ddd_hexagonal.md](docs/arquitectura/ddd_hexagonal.md) |
| Consultar endpoints de la API REST | [docs/api/endpoints_rest.md](docs/api/endpoints_rest.md) |
| Configurar Django (base, dev, prod) | [docs/configuracion/django_settings.md](docs/configuracion/django_settings.md) |
| Desplegar con Docker Compose | [docs/configuracion/docker_despliegue.md](docs/configuracion/docker_despliegue.md) |
| Pipeline CI en GitHub Actions | [docs/pipeline/ci_github.md](docs/pipeline/ci_github.md) |
| Modelo de dominio y seguridad | [docs/seguridad/dominio_vulnerabilidades.md](docs/seguridad/dominio_vulnerabilidades.md) |

## Descripcion

Dashboard para rastrear ejecuciones de pipelines CI/CD y vulnerabilidades de seguridad detectadas durante el proceso. Implementado con Django 5.x + Django REST Framework siguiendo arquitectura DDD Hexagonal. El dominio es puro Python sin dependencias de framework.

## Stack Tecnico

| Componente | Tecnologia | Version |
| :--- | :--- | :--- |
| Lenguaje | Python | >=3.10 |
| Framework Web | Django + DRF | 5.x / 3.15 |
| Tareas Asincronas | Celery + Redis | 5.3+ |
| Base de Datos (prod) | PostgreSQL | 16 |
| Base de Datos (dev) | SQLite | 3 |
| Servidor WSGI | Gunicorn | 22.x |
| Contenedores | Docker + Compose | multi-stage |
| CI/CD | GitHub Actions | v4 |
| Linter | Ruff | 0.8+ |
| Tests | pytest + pytest-django | 8.x / 4.9+ |

## Estructura del Proyecto

```
src/
  domain/           # Puro Python, SIN Django
    pipeline/       # Bounded Context: Pipeline CI/CD
    vulnerability/  # Bounded Context: Vulnerabilidades
  application/      # Casos de uso y puertos (ABC)
    ports/          # Interfaces: repositories, notifiers, scanners
    use_cases/      # Logica de aplicacion
  infrastructure/   # Adaptadores Django
    django_app/     # Settings, URLs, WSGI, Celery
    persistence/    # ORM Models, Repositories Django
    web/api/        # DRF Serializers, Views, URLs
    tasks/          # Celery Tasks
    notifiers/      # Email Notifier
  shared/           # Base Entity, Value Object, Domain Event
tests/
  unit/domain/      # Tests dominio puro (sin Django)
  unit/application/ # Tests use cases (mock repos)
  integration/      # Tests repositorios con DB
```

## Inicio Rapido

```bash
pip install -e ".[dev]"
python manage.py migrate
python manage.py runserver
```

Endpoints disponibles en `http://localhost:8000/api/`.

## Tests

| Comando | Alcance | Requisitos |
| :--- | :--- | :--- |
| `pytest tests/unit/` | Dominio + Aplicacion | Ninguno (puro Python) |
| `pytest tests/integration/` | Repositorios Django | Base de datos configurada |
| `pytest --cov=src` | Cobertura completa | Todos los requisitos |

## Resolucion de Errores

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| `pip install` se congela con backtracking | Conflicto de versiones entre dependencias | Verificar `requires-python` coincide con `python --version`; usar constraints exactos en `pyproject.toml` |
| `ModuleNotFoundError: src.infrastructure` | Paquete no instalado en modo editable | Ejecutar `pip install -e .` desde la raiz del proyecto |
| `django.db.utils.OperationalError` | PostgreSQL no disponible | Usar `development.py` (SQLite) o levantar `docker compose up db` |
| Tests de integracion fallan sin DB | `DJANGO_SETTINGS_MODULE` no apunta a settings con DB | Exportar `DJANGO_SETTINGS_MODULE=src.infrastructure.django_app.settings.development` |
| Celery no descubre tareas | Modulo de tareas no registrado | Verificar `autodiscover_tasks(["src.infrastructure.tasks"])` en `celery.py` |

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
