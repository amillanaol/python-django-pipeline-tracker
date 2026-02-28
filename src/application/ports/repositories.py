from abc import ABC, abstractmethod

from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.value_objects import PipelineStatus, Severity
from src.domain.vulnerability.entities import Vulnerability
from src.domain.vulnerability.value_objects import RemediationStatus


class IPipelineRepository(ABC):
    @abstractmethod
    def save(self, pipeline_run: PipelineRun) -> None: ...

    @abstractmethod
    def find_by_id(self, pipeline_id: str) -> PipelineRun | None: ...

    @abstractmethod
    def find_all(self) -> list[PipelineRun]: ...

    @abstractmethod
    def find_by_status(self, status: PipelineStatus) -> list[PipelineRun]: ...


class IVulnerabilityRepository(ABC):
    @abstractmethod
    def save(self, vulnerability: Vulnerability) -> None: ...

    @abstractmethod
    def find_by_id(self, vulnerability_id: str) -> Vulnerability | None: ...

    @abstractmethod
    def find_by_pipeline_run_id(self, pipeline_run_id: str) -> list[Vulnerability]: ...

    @abstractmethod
    def find_by_status(self, status: RemediationStatus) -> list[Vulnerability]: ...

    @abstractmethod
    def count_by_severity(self) -> dict[Severity, int]: ...
