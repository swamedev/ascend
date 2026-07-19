from dataclasses import dataclass


@dataclass
class MissionDTO:
    id: str
    title: str
    objective: str
    difficulty: int
    xp_reward: int
    status: str
