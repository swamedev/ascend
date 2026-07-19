from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str = ""
    weight: float = 1.0
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"skill-{self.name.lower().replace(' ', '-')}"
