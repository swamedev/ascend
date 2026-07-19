from pathlib import Path
from typing import List

from ascend.domain.builder import Builder
from ascend.runtime.kernel import RuntimeKernel
from ascend.runtime.report import ExecutionReport
from ascend.shared.clock import SystemClock


class Runtime:
    def __init__(self) -> None:
        self._kernel = RuntimeKernel()

    def run(
        self,
        package: str | Path,
        builder: str | Builder,
        evidence: str | dict[str, str] | None = None,
    ) -> ExecutionReport:
        pkg_path = Path(package)

        b: Builder
        if isinstance(builder, Builder):
            b = builder
        else:
            b = Builder(builder)

        ev_input: dict[str, str] = {}
        if evidence is not None:
            if isinstance(evidence, dict):
                ev_input = evidence
            else:
                ev_path = Path(evidence)
                if ev_path.exists():
                    ev_input = {"_default": ev_path.read_text(encoding="utf-8")}
                else:
                    ev_input = {"_default": evidence}

        report = self._kernel.run(
            package_path=pkg_path,
            builder=b,
            evidence_input=ev_input,
        )
        return report
