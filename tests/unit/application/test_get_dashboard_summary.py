from src.application.use_cases.get_dashboard_summary import GetDashboardSummaryUseCase
from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.value_objects import CveId, PipelineStatus, Severity
from src.domain.vulnerability.entities import Vulnerability
from src.domain.vulnerability.value_objects import CvssScore
from tests.conftest import InMemoryPipelineRepository, InMemoryVulnerabilityRepository


class TestGetDashboardSummaryUseCase:
    def test_empty_dashboard(
        self,
        pipeline_repo: InMemoryPipelineRepository,
        vulnerability_repo: InMemoryVulnerabilityRepository,
    ):
        use_case = GetDashboardSummaryUseCase(
            pipeline_repository=pipeline_repo,
            vulnerability_repository=vulnerability_repo,
        )
        summary = use_case.execute()
        assert summary.total_pipelines == 0
        assert summary.open_vulnerabilities == 0

    def test_dashboard_with_data(
        self,
        pipeline_repo: InMemoryPipelineRepository,
        vulnerability_repo: InMemoryVulnerabilityRepository,
    ):
        p1 = PipelineRun(id="p1", repository_name="r", branch="main", commit_sha="a")
        p1.start()
        p1.complete()
        pipeline_repo.save(p1)

        p2 = PipelineRun(id="p2", repository_name="r", branch="dev", commit_sha="b")
        p2.start()
        pipeline_repo.save(p2)

        vuln = Vulnerability(
            id="v1",
            cve_id=CveId(value="CVE-2024-12345"),
            title="Vuln",
            severity=Severity.CRITICAL,
            cvss_score=CvssScore(value=9.8),
            package_name="lib",
            package_version="1.0",
            pipeline_run_id="p1",
        )
        vulnerability_repo.save(vuln)

        use_case = GetDashboardSummaryUseCase(
            pipeline_repository=pipeline_repo,
            vulnerability_repository=vulnerability_repo,
        )
        summary = use_case.execute()
        assert summary.total_pipelines == 2
        assert summary.pipelines_by_status["SUCCESS"] == 1
        assert summary.pipelines_by_status["RUNNING"] == 1
        assert summary.vulnerabilities_by_severity["CRITICAL"] == 1
        assert summary.open_vulnerabilities == 1
