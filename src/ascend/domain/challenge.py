from dataclasses import dataclass, field
from typing import List


@dataclass
class Challenge:
    description: str
    requirements: List[str] = field(default_factory=list)
    validation_rules: List[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            import hashlib
            self.id = f"challenge-{hashlib.md5(self.description.encode()).hexdigest()[:8]}"
