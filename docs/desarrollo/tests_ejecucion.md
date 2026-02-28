# Tests

| Necesidad | Ubicacion |
| :--- | :--- |
| Comandos de ejecucion | [Comandos de Ejecucion](#comandos-de-ejecucion) |
| Descripcion de tipos de tests | [Descripcion de Tests](#descripcion-de-tests) |
| Marcadores disponibles | [Marcadores de Tests](#marcadores-de-tests) |
| Configuracion de tests | [Configuracion](#configuracion) |

Documentacion detallada de ejecucion de tests del proyecto Pipeline Tracker.

## Comandos de Ejecucion

| Comando | Alcance | Requisitos |
| :--- | :--- | :--- |
| pytest tests/unit/ | Dominio + Aplicacion (tests unitarios, puro Python sin Django) | Ninguno |
| pytest tests/integration/ | Repositorios Django (tests de integracion con DB) | Base de datos configurada |
| pytest --cov=src | Cobertura completa de codigo | Todos los requisitos |

## Descripcion de Tests

El proyecto cuenta con tres tipos de tests:

- **Tests Unitarios** (`tests/unit/`): Prueban el dominio y aplicacion sin dependencias de frameworks. No requieren base de datos ni configuracion especial. Ejecutan rapidamente y validan la logica de negocio pura.

- **Tests de Integracion** (`tests/integration/`): Prueban los repositorios Django y la interaccion con la base de datos. Requieren que Django este configurado y la base de datos accessible (SQLite en desarrollo, PostgreSQL en produccion).

- **Cobertura** (`--cov=src`): Genera reporte de cobertura de codigo. Muestra que porcentaje del codigo fuente esta siendo probado por los tests.

## Marcadores de Tests

| Marcador | Descripcion |
| :--- | :--- |
| @pytest.mark.unit | Tests unitarios (sin Django, sin DB) |
| @pytest.mark.integration | Tests de integracion (requiere DB) |

## Ejecucion Rapida

```bash
# Tests unitarios solo
pytest tests/unit/ -v

# Tests de integracion
pytest tests/integration/ -v

# Cobertura
pytest --cov=src tests/
```

## Configuracion

Los tests unitarios no requieren ninguna configuracion especial. Los tests de integracion requieren que la variable de entorno `DJANGO_SETTINGS_MODULE` apunte a un settings con base de datos configurada:

```bash
export DJANGO_SETTINGS_MODULE=src.infrastructure.django_app.settings.development
pytest tests/integration/ -v
```

En desarrollo, Django usa SQLite por defecto, por lo que los tests de integracion pueden ejecutarse directamente sin configuracion adicional.

## Control de versiones

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol(https://orcid.org/0009-0003-1768-7048) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-28 |
