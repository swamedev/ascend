from typing import List, Protocol

from ascend.domain.events import DomainEvent


class EventBus(Protocol):
    def publish(self, events: List[DomainEvent]) -> None: ...
