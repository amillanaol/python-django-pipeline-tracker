import logging

from django.conf import settings
from django.core.mail import send_mail

from src.application.ports.notifiers import IAlertNotifier
from src.domain.vulnerability.entities import Vulnerability

logger = logging.getLogger(__name__)


class EmailAlertNotifier(IAlertNotifier):
    def notify_critical_vulnerability(self, vulnerability: Vulnerability) -> None:
        subject = (
            f"[SECURITY ALERT] {vulnerability.severity.value}: "
            f"{vulnerability.cve_id.value} in {vulnerability.package_name}"
        )
        message = (
            f"A {vulnerability.severity.value} vulnerability has been detected.\n\n"
            f"CVE: {vulnerability.cve_id.value}\n"
            f"Title: {vulnerability.title}\n"
            f"Package: {vulnerability.package_name}@{vulnerability.package_version}\n"
            f"CVSS Score: {vulnerability.cvss_score.value}\n"
            f"Fix Version: {vulnerability.fix_version or 'N/A'}\n"
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
                recipient_list=getattr(settings, "ALERT_RECIPIENTS", []),
                fail_silently=True,
            )
        except Exception:
            logger.exception("Failed to send vulnerability alert email")

    def notify_pipeline_failure(self, pipeline_id: str, reason: str) -> None:
        subject = f"[PIPELINE FAILED] Pipeline {pipeline_id}"
        message = f"Pipeline {pipeline_id} has failed.\n\nReason: {reason}\n"
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
                recipient_list=getattr(settings, "ALERT_RECIPIENTS", []),
                fail_silently=True,
            )
        except Exception:
            logger.exception("Failed to send pipeline failure alert email")
