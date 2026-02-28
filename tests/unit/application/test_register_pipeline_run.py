from src.application.use_cases.register_pipeline_run import (
    RegisterPipelineRunCommand,
    RegisterPipelineRunUseCase,
)
from src.domain.pipeline.value_objects import PipelineStatus
from tests.conftest import InMemoryPipelineRepository


class TestRegisterPipelineRunUseCase:
    def test_registers_and_starts_pipeline(self, pipeline_repo: InMemoryPipelineRepository):
        use_case = RegisterPipelineRunUseCase(pipeline_repository=pipeline_repo)
        result = use_case.execute(
            RegisterPipelineRunCommand(
                repository_name="org/repo",
                branch="main",
                commit_sha="abc123",
            )
        )
        assert result.repository_name == "org/repo"
        assert result.branch == "main"
        assert result.commit_sha == "abc123"
        assert result.status == PipelineStatus.RUNNING
        assert result.started_at is not None

        saved = pipeline_repo.find_by_id(result.id)
        assert saved is not None
        assert saved.status == PipelineStatus.RUNNING
