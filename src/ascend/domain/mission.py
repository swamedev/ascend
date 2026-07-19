from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .evidence import Evidence


class MissionStatus(Enum):
    AVAILABLE = "available"
    STARTED = "started"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    COMPLETED = "completed"


@dataclass
class Mission:
    title: str
    objective: str = ""
    difficulty: int = 1
    xp_reward: int = 100
    prerequisites: List[str] = field(default_factory=list)
    id: str = ""
    status: MissionStatus = MissionStatus.AVAILABLE
    evidence_list: List[Evidence] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = f"mission-{self.title.lower().replace(' ', '-')}"

    def start(self) -> None:
        if self.status != MissionStatus.AVAILABLE:
            raise ValueError(f"Cannot start mission in status {self.status.value}")
        self.status = MissionStatus.STARTED

    def submit(self, evidence: Evidence) -> None:
        if self.status != MissionStatus.STARTED:
            raise ValueError(f"Cannot submit evidence for mission in status {self.status.value}")
        self.evidence_list.append(evidence)
        self.status = MissionStatus.EVIDENCE_SUBMITTED

    def complete(self) -> None:
        if self.status != MissionStatus.EVIDENCE_SUBMITTED:
            raise ValueError(f"Cannot complete mission in status {self.status.value}")
        self.status = MissionStatus.COMPLETED

    @property
    def is_active(self) -> bool:
        return self.status == MissionStatus.STARTED

    @property
    def is_completed(self) -> bool:
        return self.status == MissionStatus.COMPLETED

    def can_start(self, completed_mission_ids: List[str]) -> bool:
        return all(pid in completed_mission_ids for pid in self.prerequisites)
