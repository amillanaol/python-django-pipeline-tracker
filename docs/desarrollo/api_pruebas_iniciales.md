# Pruebas Iniciales de la API REST

| Necesidad | Ubicacion |
| :--- | :--- |
| Preparar la base de datos antes de probar | [Migraciones](#migraciones) |
| Entender la interfaz web de DRF | [Browsable API](#browsable-api) |
| Probar endpoints de pipelines | [Pipelines](#pipeline-endpoints) |
| Probar endpoints de vulnerabilidades | [Vulnerabilidades](#vulnerability-endpoints) |
| Probar el dashboard | [Dashboard](#dashboard-endpoint) |
| Resolver errores comunes | [Resolucion de Errores](#resolucion-de-errores) |

## Prerequisitos

| Componente | Comando de Verificacion | Resultado Esperado |
| :--- | :--- | :--- |
| Servidor activo | `python manage.py runserver 8181` | `Starting development server at http://127.0.0.1:8181/` |
| Base de datos migrada | `python manage.py showmigrations persistence` | `[X] 0001_initial` |
| Acceso a API Root | Navegador en `http://127.0.0.1:8181/api/` | JSON con enlaces a `pipelines` y `vulnerabilities` |

## Migraciones

El error `OperationalError: no such table: pipeline_runs` indica que las tablas no existen en la base de datos. La migracion `0001_initial.py` en `src/infrastructure/persistence/migrations/` crea las tablas `pipeline_runs` y `vulnerabilities`.

| Paso | Comando | Descripcion |
| :--- | :--- | :--- |
| 1 | `python manage.py makemigrations` | Genera archivos de migracion si hay cambios pendientes en modelos |
| 2 | `python manage.py migrate` | Aplica todas las migraciones y crea las tablas en la base de datos |
| 3 | `python manage.py showmigrations persistence` | Verifica que `0001_initial` aparece marcado con `[X]` |

Tablas creadas por la migracion inicial:

| Tabla | Modelo ORM | Archivo |
| :--- | :--- | :--- |
| `pipeline_runs` | `PipelineRunModel` | `src/infrastructure/persistence/models.py` |
| `vulnerabilities` | `VulnerabilityModel` | `src/infrastructure/persistence/models.py` |

## Browsable API

Django REST Framework incluye una interfaz web interactiva accesible desde el navegador. Al visitar `http://127.0.0.1:8181/api/` se muestra el **Api Root** con los endpoints disponibles.

| Elemento de la Interfaz | Funcion |
| :--- | :--- |
| Titulo `Api Root` | Punto de entrada raiz de la API |
| Respuesta JSON | Muestra los endpoints disponibles como enlaces navegables |
| Boton `GET` (azul) | Ejecuta una peticion GET al endpoint actual |
| Boton `OPTIONS` | Muestra metodos HTTP permitidos y estructura de datos esperada |
| Formularios HTML (en sub-endpoints) | Permiten enviar datos POST directamente desde el navegador |

Respuesta del Api Root en `GET /api/`:

| Clave | URL | Descripcion |
| :--- | :--- | :--- |
| `pipelines` | `http://127.0.0.1:8181/api/pipelines/` | CRUD de ejecuciones de pipeline |
| `vulnerabilities` | `http://127.0.0.1:8181/api/vulnerabilities/` | CRUD de vulnerabilidades detectadas |

El endpoint `GET /api/dashboard/` no aparece en el Api Root porque es una vista personalizada (no un ViewSet registrado en el router). Se accede directamente por URL.

## Pipeline Endpoints

### Crear un Pipeline Run

**POST /api/pipelines/** — Crea un pipeline y lo transiciona a estado `RUNNING`.

| Campo | Tipo | Requerido | Ejemplo |
| :--- | :--- | :--- | :--- |
| `repository_name` | string (max 255) | Si | `amillanaol/python-pipeline-tracker` |
| `branch` | string (max 255) | Si | `main` |
| `commit_sha` | string (max 40) | Si | `5ad2b05` |

Prueba con curl:

```bash
curl -X POST http://127.0.0.1:8181/api/pipelines/ \
  -H "Content-Type: application/json" \
  -d '{"repository_name": "amillanaol/python-pipeline-tracker", "branch": "main", "commit_sha": "5ad2b05abc123def456"}'
```

Respuesta esperada (`201 Created`): JSON con `id` (UUID), `status: "RUNNING"`, `started_at` con timestamp, `finished_at: null`, `vulnerabilities_count: 0`.

### Listar Pipelines

**GET /api/pipelines/** — Retorna todos los pipeline runs ordenados por `created_at` descendente. Paginacion: 20 por pagina.

```bash
curl http://127.0.0.1:8181/api/pipelines/
```

### Detalle de un Pipeline

**GET /api/pipelines/{id}/** — Retorna `200` con detalle o `404` si no existe.

```bash
curl http://127.0.0.1:8181/api/pipelines/{id}/
```

Reemplazar `{id}` con el UUID retornado al crear el pipeline.

## Vulnerability Endpoints

### Registrar una Vulnerabilidad

**POST /api/vulnerabilities/** — Requiere un `pipeline_run_id` existente.

| Campo | Tipo | Requerido | Ejemplo |
| :--- | :--- | :--- | :--- |
| `pipeline_run_id` | string | Si | UUID del pipeline creado previamente |
| `cve_id` | string (max 20) | Si | `CVE-2024-12345` |
| `title` | string (max 500) | Si | `SQL Injection in login` |
| `description` | string | No | `Allows unauthenticated SQL injection` |
| `severity` | string | Si | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` |
| `cvss_score` | float | Si | `9.8` |
| `package_name` | string (max 255) | Si | `django` |
| `package_version` | string (max 50) | Si | `4.2.0` |
| `fix_version` | string (max 50) | No | `4.2.8` |

```bash
curl -X POST http://127.0.0.1:8181/api/vulnerabilities/ \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_run_id": "REEMPLAZAR_CON_UUID",
    "cve_id": "CVE-2024-12345",
    "title": "SQL Injection in login",
    "severity": "CRITICAL",
    "cvss_score": 9.8,
    "package_name": "django",
    "package_version": "4.2.0",
    "fix_version": "4.2.8"
  }'
```

### Listar Vulnerabilidades

**GET /api/vulnerabilities/** — Filtrable por query params.

| Query Param | Default | Ejemplo |
| :--- | :--- | :--- |
| `pipeline_run_id` | -- | `?pipeline_run_id=UUID` |
| `status` | `OPEN` | `?status=RESOLVED` |

### Resolver una Vulnerabilidad

**POST /api/vulnerabilities/{id}/resolve/**

```bash
curl -X POST http://127.0.0.1:8181/api/vulnerabilities/{id}/resolve/ \
  -H "Content-Type: application/json" \
  -d '{"resolved_by": "amillanaol"}'
```

Retorna la vulnerabilidad con `remediation_status: "RESOLVED"` y `resolved_at` con timestamp.

## Dashboard Endpoint

**GET /api/dashboard/** — Estadisticas agregadas.

```bash
curl http://127.0.0.1:8181/api/dashboard/
```

| Campo Response | Tipo | Descripcion |
| :--- | :--- | :--- |
| `total_pipelines` | int | Total de pipeline runs registrados |
| `pipelines_by_status` | dict | Conteo por estado (`PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `CANCELLED`) |
| `vulnerabilities_by_severity` | dict | Conteo por severidad (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`) |
| `open_vulnerabilities` | int | Vulnerabilidades con status `OPEN` |

## Flujo de Prueba Recomendado

| Paso | Accion | Endpoint | Verificacion |
| :--- | :--- | :--- | :--- |
| 1 | Ejecutar migraciones | Terminal: `python manage.py migrate` | Sin errores, tablas creadas |
| 2 | Crear un pipeline | `POST /api/pipelines/` | Respuesta `201`, obtener el `id` |
| 3 | Listar pipelines | `GET /api/pipelines/` | El pipeline creado aparece en la lista |
| 4 | Registrar vulnerabilidad | `POST /api/vulnerabilities/` | Respuesta `201`, usar el `id` del pipeline |
| 5 | Listar vulnerabilidades | `GET /api/vulnerabilities/` | La vulnerabilidad aparece con status `OPEN` |
| 6 | Resolver vulnerabilidad | `POST /api/vulnerabilities/{id}/resolve/` | `remediation_status` cambia a `RESOLVED` |
| 7 | Consultar dashboard | `GET /api/dashboard/` | Estadisticas reflejan los datos creados |

## Resolucion de Errores

| Sintoma | Causa Raiz | Solucion Tecnica |
| :--- | :--- | :--- |
| `OperationalError: no such table: pipeline_runs` | Migraciones no aplicadas a la base de datos | `python manage.py makemigrations && python manage.py migrate` |
| `404 Not Found` en `/api/pipelines/{id}/` | UUID inexistente o mal formateado | Verificar el `id` retornado al crear el pipeline |
| `400 Bad Request` en POST | Campos requeridos faltantes o tipos incorrectos | Revisar tabla de campos requeridos del endpoint |
| Api Root no muestra `dashboard` | Vista personalizada, no registrada en el router DRF | Acceder directamente a `http://127.0.0.1:8181/api/dashboard/` |
| `Connection refused` al acceder a la API | Servidor no iniciado o puerto incorrecto | `python manage.py runserver 8181` |

## Archivos Clave

| Archivo | Funcion |
| :--- | :--- |
| `src/infrastructure/web/api/views.py` | ViewSets de pipelines, vulnerabilidades y dashboard |
| `src/infrastructure/web/api/serializers.py` | Serializadores DRF para request/response |
| `src/infrastructure/web/api/urls.py` | Configuracion del router y rutas API |
| `src/infrastructure/persistence/models.py` | Modelos ORM (`PipelineRunModel`, `VulnerabilityModel`) |
| `src/infrastructure/persistence/migrations/0001_initial.py` | Migracion inicial que crea las tablas |
| `src/infrastructure/django_app/settings/base.py` | Configuracion de DRF, base de datos y middleware |

Documentacion relacionada: [Endpoints REST](../api/endpoints_rest.md), [Instalacion Local](./instalacion_local.md).

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
