from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Assessment:
    evidence_id: str
    score: float = 0.0
    feedback: str = ""
    reviewer: str = ""
    id: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.id:
            self.id = f"assess-{self.evidence_id}"

    @property
    def is_approved(self) -> bool:
        return self.score >= 0.7

    @property
    def is_excellent(self) -> bool:
        return self.score >= 0.9
