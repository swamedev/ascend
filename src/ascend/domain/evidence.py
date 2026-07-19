from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EvidenceType(Enum):
    CODE = "code"
    DOCUMENT = "document"
    PROJECT = "project"
    REPORT = "report"
    VIDEO = "video"
    EXPERIMENT = "experiment"
    PRESENTATION = "presentation"
    ANALYSIS = "analysis"


class EvidenceStatus(Enum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class Evidence:
    artifact: str
    type: EvidenceType = EvidenceType.DOCUMENT
    id: str = ""
    builder_id: str = ""
    mission_id: str = ""
    status: EvidenceStatus = EvidenceStatus.SUBMITTED
    submitted_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.id:
            import hashlib
            raw = f"{self.artifact}{datetime.now().isoformat()}"
            self.id = f"ev-{hashlib.md5(raw.encode()).hexdigest()[:12]}"

    def submit(self, builder_id: str) -> None:
        self.builder_id = builder_id
        self.status = EvidenceStatus.SUBMITTED
        self.submitted_at = datetime.now()

    def accept(self) -> None:
        self.status = EvidenceStatus.ACCEPTED

    def reject(self) -> None:
        self.status = EvidenceStatus.REJECTED

    @property
    def is_pending(self) -> bool:
        return self.status == EvidenceStatus.SUBMITTED
