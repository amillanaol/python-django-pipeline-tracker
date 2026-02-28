from dataclasses import dataclass

from src.application.ports.repositories import IPipelineRepository
from src.domain.pipeline.aggregates import PipelineAggregate
from src.domain.pipeline.entities import PipelineRun


@dataclass
class RegisterPipelineRunCommand:
    repository_name: str
    branch: str
    commit_sha: str


class RegisterPipelineRunUseCase:
    def __init__(self, pipeline_repository: IPipelineRepository) -> None:
        self._pipeline_repository = pipeline_repository

    def execute(self, command: RegisterPipelineRunCommand) -> PipelineRun:
        pipeline_run = PipelineRun(
            repository_name=command.repository_name,
            branch=command.branch,
            commit_sha=command.commit_sha,
        )
        aggregate = PipelineAggregate(root=pipeline_run)
        aggregate.start_pipeline()
        self._pipeline_repository.save(aggregate.root)
        return aggregate.root
