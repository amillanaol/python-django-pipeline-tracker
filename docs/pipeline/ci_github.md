# Pipeline CI - GitHub Actions

| Necesidad | Ubicacion |
| :--- | :--- |
| Jobs del pipeline | [Jobs](#jobs) |
| Configuracion de PostgreSQL en CI | [Job: test](#job-test) |
| Cuando se ejecuta | [Triggers](#triggers) |

## Archivo

`.github/workflows/ci.yml`

## Triggers

| Evento | Ramas |
| :--- | :--- |
| `push` | `main` |
| `pull_request` | `main` |

## Jobs

| Job | Runner | Depende de | Proposito |
| :--- | :--- | :--- | :--- |
| `lint` | `ubuntu-latest` | Ninguno | Ruff check sobre `src/` |
| `test` | `ubuntu-latest` | Ninguno | Unit tests + Integration tests |
| `docker` | `ubuntu-latest` | `lint`, `test` | Build de imagen Docker |

## Job: lint

| Paso | Comando |
| :--- | :--- |
| Checkout | `actions/checkout@v4` |
| Setup Python | `actions/setup-python@v5` (3.11) |
| Install ruff | `pip install ruff` |
| Lint | `ruff check src/` |

## Job: test

Servicio PostgreSQL configurado como service container:

| Parametro | Valor |
| :--- | :--- |
| Imagen | `postgres:16-alpine` |
| `POSTGRES_DB` | `pipeline_tracker_test` |
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_PASSWORD` | `postgres` |
| Puerto | `5432:5432` |
| Healthcheck | `pg_isready` cada 10s, 5 retries |

| Paso | Comando | Variables de Entorno |
| :--- | :--- | :--- |
| Checkout | `actions/checkout@v4` | -- |
| Setup Python | `actions/setup-python@v5` (3.11) | -- |
| Install deps | `pip install ".[dev]"` | -- |
| Unit tests | `pytest tests/unit/ -v --tb=short` | -- |
| Integration tests | `pytest tests/integration/ -v --tb=short` | `DJANGO_SETTINGS_MODULE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` |

Los unit tests se ejecutan sin Django ni base de datos. Los integration tests requieren las variables de entorno del servicio PostgreSQL.

## Job: docker

| Paso | Comando |
| :--- | :--- |
| Checkout | `actions/checkout@v4` |
| Build | `docker build -f docker/Dockerfile -t pipeline-tracker:ci .` |

Este job solo valida que la imagen se construye correctamente. No realiza push a ningun registry.

## Resolucion de Errores

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| `ruff check` falla | Codigo no cumple reglas `E, F, I, N, W, UP` | Ejecutar `ruff check src/ --fix` localmente |
| Tests de integracion fallan en CI | Servicio PostgreSQL no esta ready | Verificar healthcheck options en `ci.yml` |
| `pip install` lento en CI | Resolver de pip backtracking | Ajustar constraints en `pyproject.toml`; ver [README - Resolucion de Errores](../../README.md#resolucion-de-errores) |

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
