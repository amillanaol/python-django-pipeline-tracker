from dataclasses import dataclass

from src.application.ports.repositories import IPipelineRepository, IVulnerabilityRepository
from src.domain.pipeline.value_objects import PipelineStatus
from src.domain.vulnerability.value_objects import RemediationStatus


@dataclass
class DashboardSummary:
    total_pipelines: int
    pipelines_by_status: dict[str, int]
    vulnerabilities_by_severity: dict[str, int]
    open_vulnerabilities: int


class GetDashboardSummaryUseCase:
    def __init__(
        self,
        pipeline_repository: IPipelineRepository,
        vulnerability_repository: IVulnerabilityRepository,
    ) -> None:
        self._pipeline_repository = pipeline_repository
        self._vulnerability_repository = vulnerability_repository

    def execute(self) -> DashboardSummary:
        all_pipelines = self._pipeline_repository.find_all()

        pipelines_by_status: dict[str, int] = {}
        for status in PipelineStatus:
            count = len([p for p in all_pipelines if p.status == status])
            pipelines_by_status[status.value] = count

        severity_counts = self._vulnerability_repository.count_by_severity()
        vulnerabilities_by_severity = {
            severity.value: count for severity, count in severity_counts.items()
        }

        open_vulns = self._vulnerability_repository.find_by_status(RemediationStatus.OPEN)

        return DashboardSummary(
            total_pipelines=len(all_pipelines),
            pipelines_by_status=pipelines_by_status,
            vulnerabilities_by_severity=vulnerabilities_by_severity,
            open_vulnerabilities=len(open_vulns),
        )
