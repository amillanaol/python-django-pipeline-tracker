from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ScanResult:
    cve_id: str
    title: str
    description: str
    severity: str
    cvss_score: float
    package_name: str
    package_version: str
    fix_version: str | None = None


class ISecurityScanner(ABC):
    @abstractmethod
    def scan_pipeline(self, repository_name: str, commit_sha: str) -> list[ScanResult]: ...
