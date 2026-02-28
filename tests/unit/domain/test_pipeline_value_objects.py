import pytest

from src.domain.pipeline.value_objects import CveId, PipelineStatus, Severity


class TestPipelineStatus:
    def test_all_statuses_exist(self):
        assert PipelineStatus.PENDING.value == "PENDING"
        assert PipelineStatus.RUNNING.value == "RUNNING"
        assert PipelineStatus.SUCCESS.value == "SUCCESS"
        assert PipelineStatus.FAILED.value == "FAILED"
        assert PipelineStatus.CANCELLED.value == "CANCELLED"


class TestSeverity:
    def test_all_severities_exist(self):
        assert Severity.CRITICAL.value == "CRITICAL"
        assert Severity.HIGH.value == "HIGH"
        assert Severity.MEDIUM.value == "MEDIUM"
        assert Severity.LOW.value == "LOW"
        assert Severity.INFO.value == "INFO"


class TestCveId:
    def test_valid_cve_id(self):
        cve = CveId(value="CVE-2024-12345")
        assert cve.value == "CVE-2024-12345"

    def test_valid_cve_id_long(self):
        cve = CveId(value="CVE-2024-123456")
        assert cve.value == "CVE-2024-123456"

    def test_invalid_cve_id_format(self):
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            CveId(value="INVALID")

    def test_invalid_cve_id_short_number(self):
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            CveId(value="CVE-2024-123")

    def test_cve_id_equality(self):
        assert CveId(value="CVE-2024-12345") == CveId(value="CVE-2024-12345")

    def test_cve_id_inequality(self):
        assert CveId(value="CVE-2024-12345") != CveId(value="CVE-2024-99999")
