from src.application.ports.repositories import IPipelineRepository
from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.value_objects import PipelineStatus
from src.infrastructure.persistence.models import PipelineRunModel


class DjangoPipelineRepository(IPipelineRepository):
    def save(self, pipeline_run: PipelineRun) -> None:
        PipelineRunModel.objects.update_or_create(
            id=pipeline_run.id,
            defaults={
                "repository_name": pipeline_run.repository_name,
                "branch": pipeline_run.branch,
                "commit_sha": pipeline_run.commit_sha,
                "status": pipeline_run.status.value,
                "started_at": pipeline_run.started_at,
                "finished_at": pipeline_run.finished_at,
                "vulnerabilities_count": pipeline_run.vulnerabilities_count,
            },
        )

    def find_by_id(self, pipeline_id: str) -> PipelineRun | None:
        try:
            model = PipelineRunModel.objects.get(id=pipeline_id)
            return self._to_entity(model)
        except PipelineRunModel.DoesNotExist:
            return None

    def find_all(self) -> list[PipelineRun]:
        return [self._to_entity(m) for m in PipelineRunModel.objects.all()]

    def find_by_status(self, status: PipelineStatus) -> list[PipelineRun]:
        return [
            self._to_entity(m)
            for m in PipelineRunModel.objects.filter(status=status.value)
        ]

    @staticmethod
    def _to_entity(model: PipelineRunModel) -> PipelineRun:
        return PipelineRun(
            id=model.id,
            repository_name=model.repository_name,
            branch=model.branch,
            commit_sha=model.commit_sha,
            status=PipelineStatus(model.status),
            started_at=model.started_at,
            finished_at=model.finished_at,
            vulnerabilities_count=model.vulnerabilities_count,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
