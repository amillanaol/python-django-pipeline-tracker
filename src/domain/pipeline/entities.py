from dataclasses import dataclass
from datetime import datetime, timezone

from src.domain.pipeline.exceptions import InvalidPipelineTransitionError
from src.domain.pipeline.value_objects import PipelineStatus
from src.shared.base_entity import BaseEntity


@dataclass(eq=False)
class PipelineRun(BaseEntity):
    repository_name: str = ""
    branch: str = ""
    commit_sha: str = ""
    status: PipelineStatus = PipelineStatus.PENDING
    started_at: datetime | None = None
    finished_at: datetime | None = None
    vulnerabilities_count: int = 0

    def start(self) -> None:
        if self.status != PipelineStatus.PENDING:
            raise InvalidPipelineTransitionError(
                self.status.value, PipelineStatus.RUNNING.value
            )
        self.status = PipelineStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def complete(self) -> None:
        if self.status != PipelineStatus.RUNNING:
            raise InvalidPipelineTransitionError(
                self.status.value, PipelineStatus.SUCCESS.value
            )
        self.status = PipelineStatus.SUCCESS
        self.finished_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def fail(self) -> None:
        if self.status != PipelineStatus.RUNNING:
            raise InvalidPipelineTransitionError(
                self.status.value, PipelineStatus.FAILED.value
            )
        self.status = PipelineStatus.FAILED
        self.finished_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def increment_vulnerabilities(self) -> None:
        self.vulnerabilities_count += 1
        self.updated_at = datetime.now(timezone.utc)
