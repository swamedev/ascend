from pathlib import Path
from typing import List

from ascend.domain.builder import Builder
from ascend.package_engine.loader import PackageLoader
from ascend.shared.clock import Clock, SystemClock

from .adapters.package_converter import PackageConverter
from .context import RuntimeContext
from .events.collector import DomainEventCollector
from .hooks import NoopHooks, RuntimeHooks
from .orchestrator import RuntimeOrchestrator
from .report import ExecutionReport


class RuntimeKernel:
    def __init__(
        self,
        clock: Clock | None = None,
        hooks: RuntimeHooks | None = None,
    ):
        self._package_loader = PackageLoader()
        self._converter = PackageConverter()
        self._orchestrator = RuntimeOrchestrator()
        self._clock = clock or SystemClock()
        self._hooks = hooks or NoopHooks()

    def run(
        self,
        package_path: str | Path,
        builder: Builder,
        evidence_input: dict[str, str] | None = None,
    ) -> ExecutionReport:
        try:
            aps_pkg, validation = self._package_loader.load(package_path)
        except (FileNotFoundError, OSError) as e:
            return ExecutionReport(
                success=False,
                package_id="",
                builder_username=builder.username,
                duration=0.0,
                journeys_completed=0,
                missions_completed=0,
                total_xp=0,
                competencies_unlocked=[],
                achievements_earned=[],
                errors=[str(e)],
            )

        if not validation.valid:
            msgs = [f"  [{e.level}] {e.rule}: {e.message}" for e in validation.errors]
            return ExecutionReport(
                success=False,
                package_id="",
                builder_username=builder.username,
                duration=0.0,
                journeys_completed=0,
                missions_completed=0,
                total_xp=0,
                competencies_unlocked=[],
                achievements_earned=[],
                errors=msgs,
            )

        runtime_pkg = self._converter.convert(aps_pkg)
        collector = DomainEventCollector()

        context = RuntimeContext(
            builder=builder,
            package=runtime_pkg,
            clock=self._clock,
            event_collector=collector,
            hooks=self._hooks,
            evidence_input=evidence_input or {},
        )

        start = self._clock.now()
        report = self._orchestrator.run(context)
        end = self._clock.now()
        report.duration = (end - start).total_seconds()

        collector.clear()
        return report
