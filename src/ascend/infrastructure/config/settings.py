from dataclasses import dataclass, field
from typing import List


@dataclass
class Settings:
    db_path: str = ":memory:"
    debug: bool = False
    capabilities: dict = field(default_factory=lambda: {
        "persistence": True,
        "event_store": True,
        "ai_runtime": False,
        "plugin_sdk": False,
    })
