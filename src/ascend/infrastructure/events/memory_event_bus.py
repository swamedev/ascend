from typing import Callable, List

from ascend.domain.events import DomainEvent


class MemoryEventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, List[Callable]] = {}
        self._published: List[DomainEvent] = []

    def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            self._published.append(event)
            key = event.event_type.value
            for callback in self._subscribers.get(key, []):
                callback(event)

    def subscribe(self, event_type: str, callback: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    @property
    def published(self) -> List[DomainEvent]:
        return list(self._published)

    def clear(self) -> None:
        self._published.clear()
        self._subscribers.clear()
