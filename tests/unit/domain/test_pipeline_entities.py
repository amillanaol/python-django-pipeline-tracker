import pytest

from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.exceptions import InvalidPipelineTransitionError
from src.domain.pipeline.value_objects import PipelineStatus


class TestPipelineRun:
    def _make_pipeline(self, **kwargs):
        defaults = {
            "repository_name": "org/repo",
            "branch": "main",
            "commit_sha": "abc123def456",
        }
        defaults.update(kwargs)
        return PipelineRun(**defaults)

    def test_initial_status_is_pending(self):
        pipeline = self._make_pipeline()
        assert pipeline.status == PipelineStatus.PENDING

    def test_start_sets_running(self):
        pipeline = self._make_pipeline()
        pipeline.start()
        assert pipeline.status == PipelineStatus.RUNNING
        assert pipeline.started_at is not None

    def test_complete_after_start(self):
        pipeline = self._make_pipeline()
        pipeline.start()
        pipeline.complete()
        assert pipeline.status == PipelineStatus.SUCCESS
        assert pipeline.finished_at is not None

    def test_fail_after_start(self):
        pipeline = self._make_pipeline()
        pipeline.start()
        pipeline.fail()
        assert pipeline.status == PipelineStatus.FAILED
        assert pipeline.finished_at is not None

    def test_cannot_start_running_pipeline(self):
        pipeline = self._make_pipeline()
        pipeline.start()
        with pytest.raises(InvalidPipelineTransitionError):
            pipeline.start()

    def test_cannot_complete_pending_pipeline(self):
        pipeline = self._make_pipeline()
        with pytest.raises(InvalidPipelineTransitionError):
            pipeline.complete()

    def test_cannot_fail_pending_pipeline(self):
        pipeline = self._make_pipeline()
        with pytest.raises(InvalidPipelineTransitionError):
            pipeline.fail()

    def test_increment_vulnerabilities(self):
        pipeline = self._make_pipeline()
        assert pipeline.vulnerabilities_count == 0
        pipeline.increment_vulnerabilities()
        assert pipeline.vulnerabilities_count == 1
        pipeline.increment_vulnerabilities()
        assert pipeline.vulnerabilities_count == 2

    def test_equality_by_id(self):
        p1 = self._make_pipeline(id="same-id")
        p2 = self._make_pipeline(id="same-id", branch="develop")
        assert p1 == p2

    def test_inequality_by_id(self):
        p1 = self._make_pipeline(id="id-1")
        p2 = self._make_pipeline(id="id-2")
        assert p1 != p2
