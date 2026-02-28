# Pipeline Tracker

Dashboard para rastrear ejecuciones de pipelines CI/CD y vulnerabilidades de seguridad.

## Descripcion

Dashboard para rastrear ejecuciones de pipelines CI/CD y vulnerabilidades de seguridad detectadas durante el proceso. Implementado con Django 5.x + Django REST Framework siguiendo arquitectura DDD Hexagonal. El dominio es puro Python sin dependencias de framework, separando claramente las capas de dominio, aplicacion e infraestructura para facilitar el testing y la mantenibilidad del codigo.

## Indice de la documentacion

| Necesidad | Ubicacion |
| :--- | :--- |
| Instalar y ejecutar localmente | [docs/desarrollo/instalacion_local.md](docs/desarrollo/instalacion_local.md) |
| Configurar variables de entorno y puerto | [docs/configuracion/env_puerto.md](docs/configuracion/env_puerto.md) |
| Probar la API por primera vez | [docs/desarrollo/api_pruebas_iniciales.md](docs/desarrollo/api_pruebas_iniciales.md) |
| Ejecutar tests | [docs/desarrollo/tests_ejecucion.md](docs/desarrollo/tests_ejecucion.md) |
| Entender la arquitectura DDD Hexagonal | [docs/arquitectura/ddd_hexagonal.md](docs/arquitectura/ddd_hexagonal.md) |
| Consultar endpoints de la API REST | [docs/api/endpoints_rest.md](docs/api/endpoints_rest.md) |
| Configurar Django (base, dev, prod) | [docs/configuracion/django_settings.md](docs/configuracion/django_settings.md) |
| Desplegar con Docker Compose | [docs/configuracion/docker_despliegue.md](docs/configuracion/docker_despliegue.md) |
| Pipeline CI en GitHub Actions | [docs/pipeline/ci_github.md](docs/pipeline/ci_github.md) |
| Resolucion de errores comunes | [docs/errores/general_resolucion.md](docs/errores/general_resolucion.md) |
| Modelo de dominio y seguridad | [docs/seguridad/dominio_vulnerabilidades.md](docs/seguridad/dominio_vulnerabilidades.md) |

## Stack Tecnico del proyecto

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
  domain/           # Puro Python, SIN dependencias de frameworks externos
    pipeline/       # Bounded Context: Pipeline CI/CD (entidades, value objects)
    vulnerability/  # Bounded Context: Vulnerabilidades (entidades, value objects)
  application/     # Casos de uso y puertos (ABC)
    ports/         # Interfaces: repositories, notifiers, scanners
    use_cases/     # Logica de aplicacion (RegisterPipelineRun, RecordVulnerability, etc.)
  infrastructure/  # Adaptadores Django
    django_app/    # Settings, URLs, WSGI, Celery
    persistence/   # ORM Models, Repositories Django
    web/api/       # DRF Serializers, Views, URLs
    tasks/         # Celery Tasks
    notifiers/     # Email Notifier
  shared/          # BaseEntity, BaseValueObject, DomainEvent
tests/
  unit/domain/     # Tests dominio puro (sin Django)
  unit/application/ # Tests use cases (mock repos)
  integration/    # Tests repositorios con DB
```

## Inicio Rapido

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Instalar dependencias
pip install -e ".[dev]"

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Levantar servidor
python manage.py runserver
```

Endpoints disponibles en http://127.0.0.1:8000/api/

Ver [docs/desarrollo/tests_ejecucion.md](docs/desarrollo/tests_ejecucion.md) para detalles sobre ejecucion de tests.

Ver [docs/errores/general_resolucion.md](docs/errores/general_resolucion.md) para errores comunes y sus soluciones.

## Control de versiones

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol(https://orcid.org/0009-0003-1768-7048) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-28 |
