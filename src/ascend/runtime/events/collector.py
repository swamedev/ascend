class DomainEventCollector:
    def __init__(self) -> None:
        self._events: list = []

    def collect(self, event: object) -> None:
        self._events.append(event)

    def collected(self) -> list:
        return list(self._events)

    def drain(self) -> list:
        events = list(self._events)
        self._events.clear()
        return events

    def clear(self) -> None:
        self._events.clear()
