import json
from datetime import datetime
from typing import Any

from ascend.domain.events import DomainEvent

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQliteEventStore(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def append(self, event: DomainEvent) -> None:
        self._execute(
            """INSERT INTO events (id, aggregate_id, aggregate_type, event_type, payload, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                event.event_id,
                event.aggregate_id,
                event.event_type.value,
                event.event_type.value,
                json.dumps(event.payload, default=str),
                event.timestamp.isoformat(),
            ),
        )

    def append_many(self, events: list[DomainEvent]) -> None:
        for event in events:
            self.append(event)

    def get_by_aggregate(self, aggregate_id: str) -> list[dict[str, Any]]:
        return self._fetch_all(
            "SELECT * FROM events WHERE aggregate_id = ? ORDER BY created_at",
            (aggregate_id,),
        )

    def list_all(self) -> list[dict[str, Any]]:
        return self._fetch_all("SELECT * FROM events ORDER BY created_at")
