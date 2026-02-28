import pytest

from src.application.ports.notifiers import IAlertNotifier
from src.application.ports.repositories import IPipelineRepository, IVulnerabilityRepository
from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.value_objects import PipelineStatus, Severity
from src.domain.vulnerability.entities import Vulnerability
from src.domain.vulnerability.value_objects import RemediationStatus


class InMemoryPipelineRepository(IPipelineRepository):
    def __init__(self) -> None:
        self._store: dict[str, PipelineRun] = {}

    def save(self, pipeline_run: PipelineRun) -> None:
        self._store[pipeline_run.id] = pipeline_run

    def find_by_id(self, pipeline_id: str) -> PipelineRun | None:
        return self._store.get(pipeline_id)

    def find_all(self) -> list[PipelineRun]:
        return list(self._store.values())

    def find_by_status(self, status: PipelineStatus) -> list[PipelineRun]:
        return [p for p in self._store.values() if p.status == status]


class InMemoryVulnerabilityRepository(IVulnerabilityRepository):
    def __init__(self) -> None:
        self._store: dict[str, Vulnerability] = {}

    def save(self, vulnerability: Vulnerability) -> None:
        self._store[vulnerability.id] = vulnerability

    def find_by_id(self, vulnerability_id: str) -> Vulnerability | None:
        return self._store.get(vulnerability_id)

    def find_by_pipeline_run_id(self, pipeline_run_id: str) -> list[Vulnerability]:
        return [v for v in self._store.values() if v.pipeline_run_id == pipeline_run_id]

    def find_by_status(self, status: RemediationStatus) -> list[Vulnerability]:
        return [v for v in self._store.values() if v.remediation_status == status]

    def count_by_severity(self) -> dict[Severity, int]:
        counts: dict[Severity, int] = {}
        for v in self._store.values():
            counts[v.severity] = counts.get(v.severity, 0) + 1
        return counts


class FakeNotifier(IAlertNotifier):
    def __init__(self) -> None:
        self.critical_notifications: list[Vulnerability] = []
        self.failure_notifications: list[tuple[str, str]] = []

    def notify_critical_vulnerability(self, vulnerability: Vulnerability) -> None:
        self.critical_notifications.append(vulnerability)

    def notify_pipeline_failure(self, pipeline_id: str, reason: str) -> None:
        self.failure_notifications.append((pipeline_id, reason))


@pytest.fixture
def pipeline_repo() -> InMemoryPipelineRepository:
    return InMemoryPipelineRepository()


@pytest.fixture
def vulnerability_repo() -> InMemoryVulnerabilityRepository:
    return InMemoryVulnerabilityRepository()


@pytest.fixture
def fake_notifier() -> FakeNotifier:
    return FakeNotifier()
