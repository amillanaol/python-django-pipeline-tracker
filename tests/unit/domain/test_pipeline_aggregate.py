from src.domain.pipeline.aggregates import PipelineAggregate
from src.domain.pipeline.entities import PipelineRun
from src.domain.pipeline.events import PipelineFailed, VulnerabilityDetected
from src.domain.pipeline.value_objects import PipelineStatus, Severity


class TestPipelineAggregate:
    def _make_aggregate(self):
        pipeline = PipelineRun(
            repository_name="org/repo",
            branch="main",
            commit_sha="abc123",
        )
        return PipelineAggregate(root=pipeline)

    def test_start_pipeline(self):
        agg = self._make_aggregate()
        agg.start_pipeline()
        assert agg.root.status == PipelineStatus.RUNNING

    def test_complete_pipeline(self):
        agg = self._make_aggregate()
        agg.start_pipeline()
        agg.complete_pipeline()
        assert agg.root.status == PipelineStatus.SUCCESS

    def test_fail_pipeline_emits_event(self):
        agg = self._make_aggregate()
        agg.start_pipeline()
        agg.fail_pipeline(reason="Build error")
        assert agg.root.status == PipelineStatus.FAILED
        events = agg.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], PipelineFailed)
        assert events[0].reason == "Build error"

    def test_register_vulnerability_emits_event(self):
        agg = self._make_aggregate()
        agg.start_pipeline()
        agg.register_vulnerability("CVE-2024-12345", Severity.CRITICAL)
        assert agg.root.vulnerabilities_count == 1
        events = agg.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], VulnerabilityDetected)
        assert events[0].severity == "CRITICAL"

    def test_collect_events_clears_list(self):
        agg = self._make_aggregate()
        agg.start_pipeline()
        agg.fail_pipeline(reason="error")
        events = agg.collect_events()
        assert len(events) == 1
        assert len(agg.collect_events()) == 0
