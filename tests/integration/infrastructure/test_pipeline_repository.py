import pytest

from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.value_objects import PipelineStatus
from src.infrastructure.persistence.pipeline_repository import DjangoPipelineRepository


@pytest.mark.django_db
class TestDjangoPipelineRepository:
    def test_save_and_find_by_id(self):
        repo = DjangoPipelineRepository()
        pipeline = PipelineRun(
            id="test-pipeline-1",
            repository_name="org/repo",
            branch="main",
            commit_sha="abc123def456",
        )
        pipeline.start()
        repo.save(pipeline)

        found = repo.find_by_id("test-pipeline-1")
        assert found is not None
        assert found.repository_name == "org/repo"
        assert found.status == PipelineStatus.RUNNING

    def test_find_by_id_returns_none(self):
        repo = DjangoPipelineRepository()
        assert repo.find_by_id("nonexistent") is None

    def test_find_all(self):
        repo = DjangoPipelineRepository()
        for i in range(3):
            pipeline = PipelineRun(
                id=f"pipeline-{i}",
                repository_name="org/repo",
                branch="main",
                commit_sha=f"sha{i}",
            )
            repo.save(pipeline)
        assert len(repo.find_all()) == 3

    def test_find_by_status(self):
        repo = DjangoPipelineRepository()
        p1 = PipelineRun(id="p1", repository_name="r", branch="m", commit_sha="a")
        p1.start()
        repo.save(p1)

        p2 = PipelineRun(id="p2", repository_name="r", branch="m", commit_sha="b")
        repo.save(p2)

        running = repo.find_by_status(PipelineStatus.RUNNING)
        assert len(running) == 1
        assert running[0].id == "p1"

    def test_update_existing(self):
        repo = DjangoPipelineRepository()
        pipeline = PipelineRun(
            id="update-test",
            repository_name="org/repo",
            branch="main",
            commit_sha="abc123",
        )
        repo.save(pipeline)
        pipeline.start()
        repo.save(pipeline)

        found = repo.find_by_id("update-test")
        assert found.status == PipelineStatus.RUNNING
