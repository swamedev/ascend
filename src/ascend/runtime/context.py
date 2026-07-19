from dataclasses import dataclass, field
from typing import Any

from ascend.domain.builder import Builder
from ascend.domain.events import DomainEvent
from ascend.shared.clock import Clock
from ascend.shared.clock import SystemClock

from .events.collector import DomainEventCollector
from .hooks import NoopHooks, RuntimeHooks
from .models import RuntimePackage


@dataclass
class RuntimeContext:
    builder: Builder
    package: RuntimePackage
    clock: Clock
    event_collector: DomainEventCollector
    hooks: RuntimeHooks
    evidence_input: dict[str, str]

    def __init__(
        self,
        builder: Builder,
        package: RuntimePackage,
        clock: Clock | None = None,
        event_collector: DomainEventCollector | None = None,
        hooks: RuntimeHooks | None = None,
        evidence_input: dict[str, str] | None = None,
    ):
        self.builder = builder
        self.package = package
        self.clock = clock or SystemClock()
        self.event_collector = event_collector or DomainEventCollector()
        self.hooks = hooks or NoopHooks()
        self.evidence_input = evidence_input or {}
