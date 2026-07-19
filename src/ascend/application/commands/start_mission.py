from dataclasses import dataclass


@dataclass
class StartMission:
    builder_id: str
    mission_id: str
