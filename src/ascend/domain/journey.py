from dataclasses import dataclass, field
from enum import Enum
from typing import List

from .mission import Mission


class JourneyStatus(Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass
class Journey:
    name: str
    objective: str = ""
    missions: List[Mission] = field(default_factory=list)
    status: JourneyStatus = JourneyStatus.AVAILABLE
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"journey-{self.name.lower().replace(' ', '-')}"
        for mission in self.missions:
            if self.status == JourneyStatus.COMPLETED:
                mission.status = MissionStatus.COMPLETED
