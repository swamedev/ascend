from dataclasses import dataclass, field
from typing import List

from .achievement import Achievement
from .competency import Competency
from .events import BuilderCreated, DomainEvent
from .evidence import Evidence
from .mission import Mission


@dataclass
class Builder:
    username: str
    id: str = ""
    level: int = 1
    xp: int = 0
    competencies: List[Competency] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)
    missions: List[Mission] = field(default_factory=list)
    evidence_list: List[Evidence] = field(default_factory=list)
    events: List[DomainEvent] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = f"builder-{self.username.lower()}"
        self.events.append(BuilderCreated(self.id, self.username))

    def start_mission(self, mission: Mission) -> None:
        mission.start()
        self.missions.append(mission)

    def submit_evidence(self, evidence: Evidence, mission: Mission) -> None:
        evidence.submit(self.id)
        mission.submit(evidence)
        self.evidence_list.append(evidence)

    def add_competency(self, competency: Competency) -> None:
        existing = [c for c in self.competencies if c.name == competency.name]
        if existing:
            existing[0].level = max(existing[0].level, competency.level)
        else:
            self.competencies.append(competency)

    def add_achievement(self, achievement: Achievement) -> None:
        if achievement not in self.achievements:
            self.achievements.append(achievement)

    def earn_achievement(self, achievement: Achievement) -> None:
        self.add_achievement(achievement)

    def add_xp(self, amount: int) -> None:
        self.xp += amount
        new_level = (self.xp // 500) + 1
        if new_level > self.level:
            self.level = new_level

    def gain_xp(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("XP cannot be negative")
        self.add_xp(amount)

    @property
    def active_missions(self) -> List[Mission]:
        return [m for m in self.missions if m.is_active]

    @property
    def completed_missions(self) -> List[Mission]:
        return [m for m in self.missions if m.is_completed]
