# Arquitectura DDD Hexagonal

| Necesidad | Ubicacion |
| :--- | :--- |
| Regla de dependencias entre capas | [Regla de Dependencias](#regla-de-dependencias) |
| Mapa de archivos por capa | [Mapa de Componentes](#mapa-de-componentes) |
| Shared Kernel | [Shared Kernel](#shared-kernel) |
| Bounded Contexts del dominio | [Bounded Contexts](#bounded-contexts) |
| Puertos y adaptadores | [Puertos y Adaptadores](#puertos-y-adaptadores) |

## Regla de Dependencias

```
Infrastructure --> Application --> Domain
```

| Capa | Importa de | No importa de | Responsabilidad |
| :--- | :--- | :--- | :--- |
| `src/domain/` | `src/shared/` | Django, DRF, Celery, infrastructure, application | Entidades, Value Objects, Agregados, Eventos, Excepciones |
| `src/application/` | `src/domain/`, `src/shared/` | Django, DRF, Celery, infrastructure | Puertos (ABC), Casos de Uso, Command DTOs |
| `src/infrastructure/` | `src/application/`, `src/domain/`, `src/shared/` | (sin restricciones) | ORM Models, DRF Views, Celery Tasks, Notifiers |

La capa `src/domain/` no contiene ningun `import` de Django, DRF, Celery ni de `src/infrastructure/`. Esta restriccion se verifica con `grep -r "django\|rest_framework\|celery" src/domain/`.

## Mapa de Componentes

| Archivo | Capa | Componente DDD | Descripcion |
| :--- | :--- | :--- | :--- |
| `src/shared/base_entity.py` | Shared | Entity Base | `id: str`, `created_at`, `updated_at`, `__eq__` por identidad |
| `src/shared/base_value_object.py` | Shared | Value Object Base | `frozen=True`, `__eq__` por valor, `__hash__` |
| `src/shared/domain_event.py` | Shared | Domain Event Base | `event_id`, `occurred_at`, `aggregate_id` |
| `src/domain/pipeline/entities.py` | Domain | Entity | `PipelineRun` con transiciones de estado |
| `src/domain/pipeline/value_objects.py` | Domain | Value Object | `PipelineStatus`, `Severity`, `CveId` |
| `src/domain/pipeline/aggregates.py` | Domain | Aggregate Root | `PipelineAggregate` gestiona ciclo de vida |
| `src/domain/pipeline/events.py` | Domain | Domain Event | `VulnerabilityDetected`, `PipelineFailed` |
| `src/domain/vulnerability/entities.py` | Domain | Entity | `Vulnerability` con transiciones de remediacion |
| `src/domain/vulnerability/value_objects.py` | Domain | Value Object | `CvssScore`, `RemediationStatus` |
| `src/domain/vulnerability/aggregates.py` | Domain | Aggregate Root | `VulnerabilityAggregate` |
| `src/domain/vulnerability/events.py` | Domain | Domain Event | `VulnerabilityResolved` |
| `src/application/ports/repositories.py` | Application | Port | `IPipelineRepository`, `IVulnerabilityRepository` |
| `src/application/ports/notifiers.py` | Application | Port | `IAlertNotifier` |
| `src/application/ports/scanners.py` | Application | Port | `ISecurityScanner` |
| `src/application/use_cases/register_pipeline_run.py` | Application | Use Case | Crea y arranca un `PipelineRun` |
| `src/application/use_cases/record_vulnerability.py` | Application | Use Case | Registra vulnerabilidad, notifica si CRITICAL/HIGH |
| `src/application/use_cases/resolve_vulnerability.py` | Application | Use Case | Resuelve vulnerabilidad por ID |
| `src/application/use_cases/get_dashboard_summary.py` | Application | Use Case (Query) | Estadisticas del dashboard |
| `src/infrastructure/persistence/models.py` | Infrastructure | ORM Model | `PipelineRunModel`, `VulnerabilityModel` |
| `src/infrastructure/persistence/pipeline_repository.py` | Infrastructure | Adapter | `DjangoPipelineRepository` implementa `IPipelineRepository` |
| `src/infrastructure/persistence/vulnerability_repository.py` | Infrastructure | Adapter | `DjangoVulnerabilityRepository` implementa `IVulnerabilityRepository` |
| `src/infrastructure/web/api/views.py` | Infrastructure | Adapter | ViewSets DRF inyectan use cases |
| `src/infrastructure/tasks/scan_pipeline.py` | Infrastructure | Adapter | Celery task orquesta `ISecurityScanner` |
| `src/infrastructure/notifiers/email_notifier.py` | Infrastructure | Adapter | `EmailAlertNotifier` implementa `IAlertNotifier` |

## Shared Kernel

`src/shared/` contiene tres clases base que todo bounded context hereda.

| Clase | Archivo | Tipo | Caracteristicas |
| :--- | :--- | :--- | :--- |
| `BaseEntity` | `base_entity.py` | `@dataclass` | `id` UUID auto-generado, igualdad por identidad |
| `BaseValueObject` | `base_value_object.py` | `@dataclass(frozen=True)` | Inmutable, igualdad por valor, hasheable |
| `DomainEvent` | `domain_event.py` | `@dataclass(frozen=True)` | `event_id` UUID, `occurred_at` UTC, `aggregate_id` |

## Bounded Contexts

### Pipeline

Modela el ciclo de vida de una ejecucion de pipeline CI/CD. Transiciones de estado validas:

| Estado Origen | Accion | Estado Destino | Evento Emitido |
| :--- | :--- | :--- | :--- |
| `PENDING` | `start()` | `RUNNING` | Ninguno |
| `RUNNING` | `complete()` | `SUCCESS` | Ninguno |
| `RUNNING` | `fail(reason)` | `FAILED` | `PipelineFailed` |
| `RUNNING` | `register_vulnerability(cve, severity)` | `RUNNING` | `VulnerabilityDetected` |

Transiciones invalidas lanzan `InvalidPipelineTransitionError`.

### Vulnerability

Modela una vulnerabilidad de seguridad detectada en un pipeline. Transiciones de remediacion:

| Estado Origen | Accion | Estado Destino | Restriccion |
| :--- | :--- | :--- | :--- |
| `OPEN` | `resolve()` | `RESOLVED` | Registra `resolved_at` |
| `OPEN` | `accept_risk()` | `ACCEPTED_RISK` | -- |
| `OPEN` | `mark_false_positive()` | `FALSE_POSITIVE` | -- |
| `RESOLVED` | Cualquier accion | Error | `VulnerabilityAlreadyResolvedError` |

## Puertos y Adaptadores

| Puerto (Interface) | Archivo | Adaptador | Archivo Adaptador |
| :--- | :--- | :--- | :--- |
| `IPipelineRepository` | `application/ports/repositories.py` | `DjangoPipelineRepository` | `infrastructure/persistence/pipeline_repository.py` |
| `IVulnerabilityRepository` | `application/ports/repositories.py` | `DjangoVulnerabilityRepository` | `infrastructure/persistence/vulnerability_repository.py` |
| `IAlertNotifier` | `application/ports/notifiers.py` | `EmailAlertNotifier` | `infrastructure/notifiers/email_notifier.py` |
| `ISecurityScanner` | `application/ports/scanners.py` | (placeholder) | `infrastructure/tasks/scan_pipeline.py` |

Los repositorios usan metodos `_to_entity()` para mapear modelos Django a entidades de dominio, garantizando que el dominio nunca depende del ORM.

| Campo | Valor |
| :--- | :--- |
| **Mantenedor** | amillanaol([https://orcid.org/0009-0003-1768-7048](https://orcid.org/0009-0003-1768-7048)) |
| **Estado** | Final |
| **Ultima Actualizacion** | 2026-02-27 |
