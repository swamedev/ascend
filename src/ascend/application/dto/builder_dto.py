from dataclasses import dataclass


@dataclass
class BuilderDTO:
    id: str
    username: str
    level: int
    xp: int
    competency_count: int = 0
    achievement_count: int = 0
    active_mission_count: int = 0
