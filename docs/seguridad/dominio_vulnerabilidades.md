# Modelo de Dominio — Vulnerabilidades y Pipelines

| Necesidad | Ubicacion |
| :--- | :--- |
| Entidad PipelineRun y sus estados | [PipelineRun](#pipelinerun) |
| Entidad Vulnerability y remediacion | [Vulnerability](#vulnerability) |
| Value Objects del dominio | [Value Objects](#value-objects) |
| Eventos de dominio | [Eventos de Dominio](#eventos-de-dominio) |
| Flujo de notificacion de alertas | [Flujo de Alertas](#flujo-de-alertas) |
| Modelo ORM en base de datos | [Modelo de Persistencia](#modelo-de-persistencia) |

## PipelineRun

Entidad definida en `src/domain/pipeline/entities.py`. Representa una ejecucion de pipeline CI/CD.

| Atributo | Tipo | Default | Descripcion |
| :--- | :--- | :--- | :--- |
| `id` | `str` (UUID) | Auto-generado | Identificador unico |
| `repository_name` | `str` | `""` | Nombre del repositorio (ej: `org/repo`) |
| `branch` | `str` | `""` | Rama del commit |
| `commit_sha` | `str` | `""` | SHA del commit |
| `status` | `PipelineStatus` | `PENDING` | Estado actual del pipeline |
| `started_at` | `datetime / None` | `None` | Timestamp de inicio |
| `finished_at` | `datetime / None` | `None` | Timestamp de finalizacion |
| `vulnerabilities_count` | `int` | `0` | Contador de vulnerabilidades detectadas |

### Maquina de Estados

| Transicion | Metodo | Precondicion | Postcondicion |
| :--- | :--- | :--- | :--- |
| PENDING -> RUNNING | `start()` | `status == PENDING` | Sets `started_at`, `updated_at` |
| RUNNING -> SUCCESS | `complete()` | `status == RUNNING` | Sets `finished_at`, `updated_at` |
| RUNNING -> FAILED | `fail()` | `status == RUNNING` | Sets `finished_at`, `updated_at` |
| Cualquier -> Error | Transicion invalida | Precondicion no cumplida | `InvalidPipelineTransitionError` |

`increment_vulnerabilities()` puede llamarse en cualquier estado. Incrementa `vulnerabilities_count` y actualiza `updated_at`.

## Vulnerability

Entidad definida en `src/domain/vulnerability/entities.py`. Representa una vulnerabilidad de seguridad detectada.

| Atributo | Tipo | Default | Descripcion |
| :--- | :--- | :--- | :--- |
| `id` | `str` (UUID) | Auto-generado | Identificador unico |
| `cve_id` | `CveId` | -- | Identificador CVE validado |
| `title` | `str` | `""` | Titulo de la vulnerabilidad |
| `description` | `str` | `""` | Descripcion detallada |
| `severity` | `Severity` | `INFO` | Nivel de severidad |
| `cvss_score` | `CvssScore` | `0.0` | Puntuacion CVSS (0.0-10.0) |
| `package_name` | `str` | `""` | Paquete afectado |
| `package_version` | `str` | `""` | Version afectada |
| `fix_version` | `str / None` | `None` | Version con el fix |
| `remediation_status` | `RemediationStatus` | `OPEN` | Estado de remediacion |
| `detected_at` | `datetime` | `now(UTC)` | Timestamp de deteccion |
| `resolved_at` | `datetime / None` | `None` | Timestamp de resolucion |
| `pipeline_run_id` | `str` | `""` | FK al PipelineRun asociado |

### Transiciones de Remediacion

| Transicion | Metodo | Precondicion | Postcondicion |
| :--- | :--- | :--- | :--- |
| OPEN -> RESOLVED | `resolve()` | `status != RESOLVED` | Sets `resolved_at`, `updated_at` |
| OPEN -> ACCEPTED_RISK | `accept_risk()` | `status != RESOLVED` | Sets `updated_at` |
| OPEN -> FALSE_POSITIVE | `mark_false_positive()` | `status != RESOLVED` | Sets `updated_at` |
| RESOLVED -> Cualquiera | Error | -- | `VulnerabilityAlreadyResolvedError` |

## Value Objects

### Pipeline Value Objects

Archivo: `src/domain/pipeline/value_objects.py`

| Value Object | Tipo | Valores / Validacion |
| :--- | :--- | :--- |
| `PipelineStatus` | Enum | `PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `CANCELLED` |
| `Severity` | Enum | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` |
| `CveId` | `BaseValueObject(frozen=True)` | Regex `^CVE-\d{4}-\d{4,}$`; lanza `ValueError` si invalido |

### Vulnerability Value Objects

Archivo: `src/domain/vulnerability/value_objects.py`

| Value Object | Tipo | Valores / Validacion |
| :--- | :--- | :--- |
| `RemediationStatus` | Enum | `OPEN`, `IN_PROGRESS`, `RESOLVED`, `ACCEPTED_RISK`, `FALSE_POSITIVE` |
| `CvssScore` | `BaseValueObject(frozen=True)` | `float` entre 0.0 y 10.0; lanza `InvalidCvssScoreError` si fuera de rango |

## Eventos de Dominio

| Evento | Archivo | Aggregate Root | Atributos |
| :--- | :--- | :--- | :--- |
| `VulnerabilityDetected` | `src/domain/pipeline/events.py` | `PipelineAggregate` | `aggregate_id`, `cve_id`, `severity` |
| `PipelineFailed` | `src/domain/pipeline/events.py` | `PipelineAggregate` | `aggregate_id`, `reason` |
| `VulnerabilityResolved` | `src/domain/vulnerability/events.py` | `VulnerabilityAggregate` | `aggregate_id`, `resolved_by` |

Los eventos se recolectan con `aggregate.collect_events()` que retorna la lista y la limpia internamente.

## Excepciones de Dominio

| Excepcion | Archivo | Cuando se lanza |
| :--- | :--- | :--- |
| `InvalidPipelineTransitionError` | `src/domain/pipeline/exceptions.py` | Transicion de estado invalida en `PipelineRun` |
| `InvalidSeverityError` | `src/domain/pipeline/exceptions.py` | Valor de severity no reconocido |
| `InvalidCvssScoreError` | `src/domain/vulnerability/exceptions.py` | CVSS score fuera del rango 0.0-10.0 |
| `VulnerabilityAlreadyResolvedError` | `src/domain/vulnerability/exceptions.py` | Intento de modificar vulnerabilidad ya resuelta |

## Flujo de Alertas

El use case `RecordVulnerabilityUseCase` (`src/application/use_cases/record_vulnerability.py`) evalua la severidad al registrar una vulnerabilidad:

| Severidad | Accion | Puerto Invocado |
| :--- | :--- | :--- |
| `CRITICAL` | Notificacion enviada | `IAlertNotifier.notify_critical_vulnerability()` |
| `HIGH` | Notificacion enviada | `IAlertNotifier.notify_critical_vulnerability()` |
| `MEDIUM` | Sin notificacion | -- |
| `LOW` | Sin notificacion | -- |
| `INFO` | Sin notificacion | -- |

El adaptador `EmailAlertNotifier` (`src/infrastructure/notifiers/email_notifier.py`) implementa el envio via `django.core.mail.send_mail`. Configurar `DEFAULT_FROM_EMAIL` y `ALERT_RECIPIENTS` en settings para activar el envio.

## Modelo de Persistencia

Modelos Django ORM en `src/infrastructure/persistence/models.py`:

| Modelo ORM | Tabla | Entidad de Dominio | FK |
| :--- | :--- | :--- | :--- |
| `PipelineRunModel` | `pipeline_runs` | `PipelineRun` | -- |
| `VulnerabilityModel` | `vulnerabilities` | `Vulnerability` | `pipeline_run_id` -> `PipelineRunModel` (CASCADE) |

Los repositorios (`DjangoPipelineRepository`, `DjangoVulnerabilityRepository`) usan `update_or_create` para persistir y metodos `_to_entity()` para mapear de ORM a entidad de dominio. Esto garantiza que el dominio nunca depende del ORM.

Admin registrado en `src/infrastructure/persistence/admin.py` con `list_display`, `list_filter` y `search_fields` para ambos modelos.

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
