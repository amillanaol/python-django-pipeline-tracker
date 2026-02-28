from rest_framework import serializers


class PipelineRunSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    repository_name = serializers.CharField(max_length=255)
    branch = serializers.CharField(max_length=255)
    commit_sha = serializers.CharField(max_length=40)
    status = serializers.CharField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)
    finished_at = serializers.DateTimeField(read_only=True, allow_null=True)
    vulnerabilities_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class VulnerabilitySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    cve_id = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(required=False, default="")
    severity = serializers.CharField(max_length=10)
    cvss_score = serializers.FloatField()
    package_name = serializers.CharField(max_length=255)
    package_version = serializers.CharField(max_length=50)
    fix_version = serializers.CharField(max_length=50, required=False, allow_null=True)
    remediation_status = serializers.CharField(read_only=True)
    detected_at = serializers.DateTimeField(read_only=True)
    resolved_at = serializers.DateTimeField(read_only=True, allow_null=True)
    pipeline_run_id = serializers.CharField()


class ResolveVulnerabilitySerializer(serializers.Serializer):
    resolved_by = serializers.CharField(max_length=255)


class DashboardSummarySerializer(serializers.Serializer):
    total_pipelines = serializers.IntegerField()
    pipelines_by_status = serializers.DictField(child=serializers.IntegerField())
    vulnerabilities_by_severity = serializers.DictField(child=serializers.IntegerField())
    open_vulnerabilities = serializers.IntegerField()
