from src.infrastructure.django_app.celery import app


@app.task(name="scan_pipeline")
def scan_pipeline_task(pipeline_run_id: str, repository_name: str, commit_sha: str) -> dict:
    """Celery task that orchestrates a security scan via ISecurityScanner.

    In a real implementation, this would inject a concrete ISecurityScanner
    and call RecordVulnerabilityUseCase for each finding.
    """
    from src.application.use_cases.record_vulnerability import (
        RecordVulnerabilityCommand,
        RecordVulnerabilityUseCase,
    )
    from src.infrastructure.notifiers.email_notifier import EmailAlertNotifier
    from src.infrastructure.persistence.pipeline_repository import DjangoPipelineRepository
    from src.infrastructure.persistence.vulnerability_repository import (
        DjangoVulnerabilityRepository,
    )

    # Placeholder: a real scanner adapter would be injected here
    scan_results: list = []

    use_case = RecordVulnerabilityUseCase(
        vulnerability_repository=DjangoVulnerabilityRepository(),
        pipeline_repository=DjangoPipelineRepository(),
        notifier=EmailAlertNotifier(),
    )

    for result in scan_results:
        use_case.execute(
            RecordVulnerabilityCommand(
                pipeline_run_id=pipeline_run_id,
                cve_id=result.cve_id,
                title=result.title,
                description=result.description,
                severity=result.severity,
                cvss_score=result.cvss_score,
                package_name=result.package_name,
                package_version=result.package_version,
                fix_version=result.fix_version,
            )
        )

    return {
        "pipeline_run_id": pipeline_run_id,
        "vulnerabilities_found": len(scan_results),
    }
