from django.contrib import admin

from src.infrastructure.persistence.models import PipelineRunModel, VulnerabilityModel


@admin.register(PipelineRunModel)
class PipelineRunAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "repository_name",
        "branch",
        "status",
        "vulnerabilities_count",
        "created_at",
    ]
    list_filter = ["status", "repository_name"]
    search_fields = ["repository_name", "branch", "commit_sha"]


@admin.register(VulnerabilityModel)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = [
        "cve_id",
        "title",
        "severity",
        "cvss_score",
        "remediation_status",
        "detected_at",
    ]
    list_filter = ["severity", "remediation_status"]
    search_fields = ["cve_id", "title", "package_name"]
