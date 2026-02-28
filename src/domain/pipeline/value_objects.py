import re
from dataclasses import dataclass
from enum import Enum

from src.shared.base_value_object import BaseValueObject


class PipelineStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


CVE_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$")


@dataclass(frozen=True)
class CveId(BaseValueObject):
    value: str

    def __post_init__(self) -> None:
        if not CVE_PATTERN.match(self.value):
            raise ValueError(
                f"Invalid CVE ID format: '{self.value}'. Expected CVE-YYYY-NNNNN."
            )
