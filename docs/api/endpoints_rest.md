# Endpoints API REST

| Necesidad | Ubicacion |
| :--- | :--- |
| Listar todos los endpoints | [Tabla de Endpoints](#tabla-de-endpoints) |
| Crear un pipeline run | [POST /api/pipelines/](#pipeline-endpoints) |
| Registrar una vulnerabilidad | [POST /api/vulnerabilities/](#vulnerability-endpoints) |
| Resolver una vulnerabilidad | [POST /api/vulnerabilities/{id}/resolve/](#resolver-vulnerabilidad) |
| Obtener resumen del dashboard | [GET /api/dashboard/](#dashboard-endpoint) |

## Tabla de Endpoints

| Metodo | Ruta | Descripcion | Archivo |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/pipelines/` | Listar todos los pipeline runs | `src/infrastructure/web/api/views.py:45` |
| `POST` | `/api/pipelines/` | Crear y arrancar un pipeline run | `src/infrastructure/web/api/views.py:51` |
| `GET` | `/api/pipelines/{id}/` | Detalle de un pipeline run | `src/infrastructure/web/api/views.py:69` |
| `GET` | `/api/vulnerabilities/` | Listar vulnerabilidades (filtrable) | `src/infrastructure/web/api/views.py:78` |
| `POST` | `/api/vulnerabilities/` | Registrar nueva vulnerabilidad | `src/infrastructure/web/api/views.py:94` |
| `GET` | `/api/vulnerabilities/{id}/` | Detalle de una vulnerabilidad | `src/infrastructure/web/api/views.py:122` |
| `POST` | `/api/vulnerabilities/{id}/resolve/` | Resolver una vulnerabilidad | `src/infrastructure/web/api/views.py:129` |
| `GET` | `/api/dashboard/` | Resumen estadistico del dashboard | `src/infrastructure/web/api/views.py:147` |

Configuracion del router DRF en `src/infrastructure/web/api/urls.py`. URL raiz incluida desde `src/infrastructure/django_app/urls.py`.

## Pipeline Endpoints

### POST /api/pipelines/

Crea un `PipelineRun` y lo transiciona a estado `RUNNING` mediante `RegisterPipelineRunUseCase`.

| Campo Request | Tipo | Requerido | Descripcion |
| :--- | :--- | :--- | :--- |
| `repository_name` | string (max 255) | Si | Nombre del repositorio (ej: `org/repo`) |
| `branch` | string (max 255) | Si | Rama del commit |
| `commit_sha` | string (max 40) | Si | SHA del commit |

Respuesta `201 Created`:

| Campo Response | Tipo | Descripcion |
| :--- | :--- | :--- |
| `id` | string (UUID) | Identificador unico |
| `repository_name` | string | Nombre del repositorio |
| `branch` | string | Rama |
| `commit_sha` | string | SHA del commit |
| `status` | string | Siempre `RUNNING` al crear |
| `started_at` | datetime | Timestamp de inicio |
| `finished_at` | datetime / null | `null` al crear |
| `vulnerabilities_count` | int | `0` al crear |
| `created_at` | datetime | Timestamp de creacion |
| `updated_at` | datetime | Timestamp de actualizacion |

### GET /api/pipelines/

Retorna lista de todos los pipeline runs ordenados por `created_at` descendente. Paginacion configurada en `REST_FRAMEWORK.PAGE_SIZE = 20`.

### GET /api/pipelines/{id}/

Retorna `200` con detalle del pipeline o `404` si no existe.

## Vulnerability Endpoints

### POST /api/vulnerabilities/

Registra una vulnerabilidad via `RecordVulnerabilityUseCase`. Incrementa `vulnerabilities_count` del pipeline asociado. Envia notificacion si severity es `CRITICAL` o `HIGH`.

| Campo Request | Tipo | Requerido | Descripcion |
| :--- | :--- | :--- | :--- |
| `pipeline_run_id` | string | Si | ID del pipeline run asociado |
| `cve_id` | string (max 20) | Si | Formato `CVE-YYYY-NNNNN` |
| `title` | string (max 500) | Si | Titulo de la vulnerabilidad |
| `description` | string | No | Descripcion detallada |
| `severity` | string | Si | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` |
| `cvss_score` | float | Si | Valor entre 0.0 y 10.0 |
| `package_name` | string (max 255) | Si | Nombre del paquete afectado |
| `package_version` | string (max 50) | Si | Version afectada |
| `fix_version` | string (max 50) | No | Version con el fix aplicado |

Respuesta `201 Created` con los campos del request mas `id`, `remediation_status` (`OPEN`), `detected_at`, `resolved_at` (`null`).

### GET /api/vulnerabilities/

| Query Param | Tipo | Default | Descripcion |
| :--- | :--- | :--- | :--- |
| `pipeline_run_id` | string | -- | Filtra por pipeline run |
| `status` | string | `OPEN` | Filtra por `RemediationStatus` |

Si se proporciona `pipeline_run_id`, tiene prioridad sobre `status`.

### Resolver Vulnerabilidad

**POST /api/vulnerabilities/{id}/resolve/**

| Campo Request | Tipo | Requerido | Descripcion |
| :--- | :--- | :--- | :--- |
| `resolved_by` | string (max 255) | Si | Identificador de quien resuelve |

Retorna `200` con la vulnerabilidad actualizada (`remediation_status: RESOLVED`, `resolved_at` con timestamp). Lanza error si la vulnerabilidad ya esta resuelta o no existe.

## Dashboard Endpoint

### GET /api/dashboard/

Retorna estadisticas agregadas via `GetDashboardSummaryUseCase`.

| Campo Response | Tipo | Descripcion |
| :--- | :--- | :--- |
| `total_pipelines` | int | Total de pipeline runs registrados |
| `pipelines_by_status` | dict[string, int] | Conteo por cada `PipelineStatus` |
| `vulnerabilities_by_severity` | dict[string, int] | Conteo por cada `Severity` |
| `open_vulnerabilities` | int | Vulnerabilidades con status `OPEN` |

## Serializers

| Serializer | Archivo | Uso |
| :--- | :--- | :--- |
| `PipelineRunSerializer` | `src/infrastructure/web/api/serializers.py:4` | Request/Response para pipelines |
| `VulnerabilitySerializer` | `src/infrastructure/web/api/serializers.py:17` | Request/Response para vulnerabilidades |
| `ResolveVulnerabilitySerializer` | `src/infrastructure/web/api/serializers.py:33` | Request para resolver vulnerabilidad |
| `DashboardSummarySerializer` | `src/infrastructure/web/api/serializers.py:37` | Response del dashboard |

## Configuracion DRF

Definida en `src/infrastructure/django_app/settings/base.py:95`:

| Parametro | Valor |
| :--- | :--- |
| `DEFAULT_PAGINATION_CLASS` | `PageNumberPagination` |
| `PAGE_SIZE` | `20` |
| `DEFAULT_FILTER_BACKENDS` | `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter` |

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
