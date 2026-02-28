from django.db import models


class PipelineRunModel(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    repository_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    commit_sha = models.CharField(max_length=40)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("RUNNING", "Running"),
            ("SUCCESS", "Success"),
            ("FAILED", "Failed"),
            ("CANCELLED", "Cancelled"),
        ],
        default="PENDING",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    vulnerabilities_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "persistence"
        db_table = "pipeline_runs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.repository_name}:{self.branch} ({self.status})"


class VulnerabilityModel(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    cve_id = models.CharField(max_length=20)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, default="")
    severity = models.CharField(
        max_length=10,
        choices=[
            ("CRITICAL", "Critical"),
            ("HIGH", "High"),
            ("MEDIUM", "Medium"),
            ("LOW", "Low"),
            ("INFO", "Info"),
        ],
    )
    cvss_score = models.FloatField(default=0.0)
    package_name = models.CharField(max_length=255)
    package_version = models.CharField(max_length=50)
    fix_version = models.CharField(max_length=50, null=True, blank=True)
    remediation_status = models.CharField(
        max_length=20,
        choices=[
            ("OPEN", "Open"),
            ("IN_PROGRESS", "In Progress"),
            ("RESOLVED", "Resolved"),
            ("ACCEPTED_RISK", "Accepted Risk"),
            ("FALSE_POSITIVE", "False Positive"),
        ],
        default="OPEN",
    )
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    pipeline_run = models.ForeignKey(
        PipelineRunModel,
        on_delete=models.CASCADE,
        related_name="vulnerabilities",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "persistence"
        db_table = "vulnerabilities"
        ordering = ["-detected_at"]

    def __str__(self) -> str:
        return f"{self.cve_id} - {self.title} ({self.severity})"
