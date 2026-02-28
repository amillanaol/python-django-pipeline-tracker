from dataclasses import dataclass, field

from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.events import PipelineFailed, VulnerabilityDetected
from src.domain.pipeline.value_objects import Severity
from src.shared.domain_event import DomainEvent


@dataclass
class PipelineAggregate:
    root: PipelineRun
    _events: list[DomainEvent] = field(default_factory=list, init=False)

    def start_pipeline(self) -> None:
        self.root.start()

    def complete_pipeline(self) -> None:
        self.root.complete()

    def fail_pipeline(self, reason: str) -> None:
        self.root.fail()
        self._events.append(
            PipelineFailed(aggregate_id=self.root.id, reason=reason)
        )

    def register_vulnerability(self, cve_id: str, severity: Severity) -> None:
        self.root.increment_vulnerabilities()
        self._events.append(
            VulnerabilityDetected(
                aggregate_id=self.root.id,
                cve_id=cve_id,
                severity=severity.value,
            )
        )

    def collect_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
