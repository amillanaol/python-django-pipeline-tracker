from abc import ABC, abstractmethod

from src.domain.vulnerability.entities import Vulnerability


class IAlertNotifier(ABC):
    @abstractmethod
    def notify_critical_vulnerability(self, vulnerability: Vulnerability) -> None: ...

    @abstractmethod
    def notify_pipeline_failure(self, pipeline_id: str, reason: str) -> None: ...
