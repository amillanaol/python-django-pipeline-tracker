# Instalacion Local

| Necesidad | Ubicacion |
| :--- | :--- |
| Requisitos previos | [Requisitos](#requisitos) |
| Instalacion paso a paso | [Instalacion](#instalacion) |
| Ejecutar tests | [Tests](#tests) |
| Levantar servidor de desarrollo | [Servidor de Desarrollo](#servidor-de-desarrollo) |

## Requisitos

| Componente | Version Minima | Proposito |
| :--- | :--- | :--- |
| Python | 3.10 | Runtime |
| pip | 21.0+ | Gestor de paquetes |
| Git | 2.x | Control de versiones |

PostgreSQL y Redis son opcionales para desarrollo local. El settings de development usa SQLite y Celery funciona sin broker (las tareas no se ejecutaran).

## Instalacion

| Paso | Comando | Descripcion |
| :--- | :--- | :--- |
| 1 | `git clone <repo-url> && cd python-pipeline-tracker` | Clonar repositorio |
| 2 | `python -m venv .venv` | Crear entorno virtual |
| 3 | `.venv/Scripts/activate` (Windows) o `source .venv/bin/activate` (Unix) | Activar entorno virtual |
| 4 | `pip install -e ".[dev]"` | Instalar proyecto en modo editable con dependencias de desarrollo |
| 5 | `python manage.py migrate` | Aplicar migraciones (SQLite en dev) |

El paso 4 instala todas las dependencias de produccion y desarrollo. Si `pip install` se congela, revisar la seccion [Resolucion de Errores](#resolucion-de-errores).

## Servidor de Desarrollo

```bash
python manage.py runserver
```

API disponible en `http://localhost:8000/api/`. Panel de admin en `http://localhost:8000/admin/` (requiere `python manage.py createsuperuser`).

`manage.py` usa `DJANGO_SETTINGS_MODULE=src.infrastructure.django_app.settings.development` por defecto, que configura SQLite y `DEBUG=True`.

## Tests

| Comando | Alcance | Requiere DB | Requiere Django |
| :--- | :--- | :--- | :--- |
| `pytest tests/unit/domain/` | Entidades, Value Objects, Agregados | No | No |
| `pytest tests/unit/application/` | Use Cases con repos in-memory | No | No |
| `pytest tests/unit/` | Todos los unit tests | No | No |
| `pytest tests/integration/` | Repositorios Django con DB | Si (SQLite en dev) | Si |
| `pytest` | Todo el suite | Si | Si |
| `pytest --cov=src` | Todo con cobertura | Si | Si |

Para tests de integracion, exportar la variable de entorno:

```bash
export DJANGO_SETTINGS_MODULE=src.infrastructure.django_app.settings.development
```

## Linting

| Comando | Proposito |
| :--- | :--- |
| `ruff check src/` | Verificar errores de lint |
| `ruff check src/ --fix` | Corregir errores automaticamente |
| `ruff format src/` | Formatear codigo |

Reglas configuradas en `pyproject.toml`: `E, F, I, N, W, UP`. Line length: 99.

## Estructura de Archivos de Test

| Archivo | Contenido |
| :--- | :--- |
| `tests/conftest.py` | `InMemoryPipelineRepository`, `InMemoryVulnerabilityRepository`, `FakeNotifier`, fixtures pytest |
| `tests/unit/domain/test_pipeline_entities.py` | Tests de `PipelineRun` (transiciones, igualdad) |
| `tests/unit/domain/test_pipeline_value_objects.py` | Tests de `PipelineStatus`, `Severity`, `CveId` |
| `tests/unit/domain/test_pipeline_aggregate.py` | Tests de `PipelineAggregate` (eventos, ciclo de vida) |
| `tests/unit/domain/test_vulnerability_entities.py` | Tests de `Vulnerability` (resolve, accept_risk, mark_false_positive) |
| `tests/unit/domain/test_vulnerability_value_objects.py` | Tests de `CvssScore`, `RemediationStatus` |
| `tests/unit/application/test_register_pipeline_run.py` | Test de `RegisterPipelineRunUseCase` |
| `tests/unit/application/test_record_vulnerability.py` | Test de `RecordVulnerabilityUseCase` (notificaciones) |
| `tests/unit/application/test_resolve_vulnerability.py` | Test de `ResolveVulnerabilityUseCase` (errores) |
| `tests/unit/application/test_get_dashboard_summary.py` | Test de `GetDashboardSummaryUseCase` (estadisticas) |
| `tests/integration/infrastructure/test_pipeline_repository.py` | Test de `DjangoPipelineRepository` con DB |
| `tests/integration/infrastructure/test_vulnerability_repository.py` | Test de `DjangoVulnerabilityRepository` con DB |

## Resolucion de Errores

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| `pip install` se congela (backtracking) | `requires-python` no coincide con version de Python instalada | Verificar `python --version` vs `requires-python` en `pyproject.toml` |
| `ModuleNotFoundError: src` | Proyecto no instalado en modo editable | Ejecutar `pip install -e .` |
| `No module named 'django'` | Entorno virtual no activado o dependencias no instaladas | Activar venv y ejecutar `pip install -e ".[dev]"` |
| Tests unitarios importan Django | Test en carpeta incorrecta o import incorrecto | Los tests en `tests/unit/` no deben importar de `src/infrastructure/` |
| `OperationalError: no such table` | Migraciones no aplicadas | Ejecutar `python manage.py migrate` |

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
