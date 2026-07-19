from dataclasses import dataclass, field
from typing import List


@dataclass
class Competency:
    name: str
    description: str = ""
    level: int = 1
    criteria: List[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"comp-{self.name.lower().replace(' ', '-')}"

    def increase_level(self) -> None:
        self.level += 1

    def check_completion(self, completed_criteria: List[str]) -> bool:
        if not self.criteria:
            return True
        matched = sum(1 for c in self.criteria if c in completed_criteria)
        return matched / len(self.criteria) >= 0.5
