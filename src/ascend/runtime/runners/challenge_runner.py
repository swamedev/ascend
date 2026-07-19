from ..context import RuntimeContext
from ..models import RuntimeMission
from ..report import MissionResult


class ChallengeRunner:
    def open(self, mission: RuntimeMission, context: RuntimeContext) -> str:
        return mission.challenge.description

    def collect_evidence(
        self, mission: RuntimeMission, context: RuntimeContext
    ) -> str:
        evidence = context.evidence_input.get(mission.id, "")
        if not evidence and mission.challenge.evidence_required:
            pass
        return evidence
