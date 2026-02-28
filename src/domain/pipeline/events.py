from dataclasses import dataclass

from src.shared.domain_event import DomainEvent


@dataclass(frozen=True)
class VulnerabilityDetected(DomainEvent):
    cve_id: str = ""
    severity: str = ""


@dataclass(frozen=True)
class PipelineFailed(DomainEvent):
    reason: str = ""
