from dataclasses import dataclass, field
from typing import List


@dataclass
class UnlockCompetency:
    builder_id: str
    name: str
    description: str = ""
    level: int = 1
    criteria: List[str] = field(default_factory=list)
