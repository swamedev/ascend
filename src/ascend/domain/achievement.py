from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Achievement:
    name: str
    description: str = ""
    criteria: List[str] = field(default_factory=list)
    badge: str = ""
    id: str = ""
    earned_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.id:
            self.id = f"ach-{self.name.lower().replace(' ', '-')}"

    def earn(self) -> None:
        self.earned_at = datetime.now()

    @property
    def is_earned(self) -> bool:
        return self.earned_at is not None
