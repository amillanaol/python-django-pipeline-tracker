from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.application.use_cases.get_dashboard_summary import GetDashboardSummaryUseCase
from src.application.use_cases.record_vulnerability import (
    RecordVulnerabilityCommand,
    RecordVulnerabilityUseCase,
)
from src.application.use_cases.register_pipeline_run import (
    RegisterPipelineRunCommand,
    RegisterPipelineRunUseCase,
)
from src.application.use_cases.resolve_vulnerability import (
    ResolveVulnerabilityCommand,
    ResolveVulnerabilityUseCase,
)
from src.infrastructure.notifiers.email_notifier import EmailAlertNotifier
from src.infrastructure.persistence.pipeline_repository import DjangoPipelineRepository
from src.infrastructure.persistence.vulnerability_repository import (
    DjangoVulnerabilityRepository,
)
from src.infrastructure.web.api.serializers import (
    DashboardSummarySerializer,
    PipelineRunSerializer,
    ResolveVulnerabilitySerializer,
    VulnerabilitySerializer,
)


def _pipeline_repo() -> DjangoPipelineRepository:
    return DjangoPipelineRepository()


def _vulnerability_repo() -> DjangoVulnerabilityRepository:
    return DjangoVulnerabilityRepository()


def _notifier() -> EmailAlertNotifier:
    return EmailAlertNotifier()


class PipelineRunViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        repo = _pipeline_repo()
        pipelines = repo.find_all()
        serializer = PipelineRunSerializer(pipelines, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = PipelineRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = RegisterPipelineRunUseCase(pipeline_repository=_pipeline_repo())
        pipeline_run = use_case.execute(
            RegisterPipelineRunCommand(
                repository_name=serializer.validated_data["repository_name"],
                branch=serializer.validated_data["branch"],
                commit_sha=serializer.validated_data["commit_sha"],
            )
        )

        return Response(
            PipelineRunSerializer(pipeline_run).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        repo = _pipeline_repo()
        pipeline = repo.find_by_id(pk)
        if not pipeline:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(PipelineRunSerializer(pipeline).data)


class VulnerabilityViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        repo = _vulnerability_repo()
        pipeline_run_id = request.query_params.get("pipeline_run_id")
        if pipeline_run_id:
            vulnerabilities = repo.find_by_pipeline_run_id(pipeline_run_id)
        else:
            from src.domain.vulnerability.value_objects import RemediationStatus

            status_filter = request.query_params.get("status")
            if status_filter:
                vulnerabilities = repo.find_by_status(RemediationStatus(status_filter))
            else:
                vulnerabilities = repo.find_by_status(RemediationStatus.OPEN)
        serializer = VulnerabilitySerializer(vulnerabilities, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = VulnerabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = RecordVulnerabilityUseCase(
            vulnerability_repository=_vulnerability_repo(),
            pipeline_repository=_pipeline_repo(),
            notifier=_notifier(),
        )
        vulnerability = use_case.execute(
            RecordVulnerabilityCommand(
                pipeline_run_id=serializer.validated_data["pipeline_run_id"],
                cve_id=serializer.validated_data["cve_id"],
                title=serializer.validated_data["title"],
                description=serializer.validated_data.get("description", ""),
                severity=serializer.validated_data["severity"],
                cvss_score=serializer.validated_data["cvss_score"],
                package_name=serializer.validated_data["package_name"],
                package_version=serializer.validated_data["package_version"],
                fix_version=serializer.validated_data.get("fix_version"),
            )
        )

        return Response(
            VulnerabilitySerializer(vulnerability).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        repo = _vulnerability_repo()
        vulnerability = repo.find_by_id(pk)
        if not vulnerability:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(VulnerabilitySerializer(vulnerability).data)

    @action(detail=True, methods=["post"])
    def resolve(self, request: Request, pk: str = None) -> Response:
        serializer = ResolveVulnerabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = ResolveVulnerabilityUseCase(
            vulnerability_repository=_vulnerability_repo(),
        )
        vulnerability = use_case.execute(
            ResolveVulnerabilityCommand(
                vulnerability_id=pk,
                resolved_by=serializer.validated_data["resolved_by"],
            )
        )

        return Response(VulnerabilitySerializer(vulnerability).data)


@api_view(["GET"])
def dashboard_summary(request: Request) -> Response:
    use_case = GetDashboardSummaryUseCase(
        pipeline_repository=_pipeline_repo(),
        vulnerability_repository=_vulnerability_repo(),
    )
    summary = use_case.execute()
    serializer = DashboardSummarySerializer(summary)
    return Response(serializer.data)
