from ascend.application.commands.complete_assessment import CompleteAssessment
from ascend.application.exceptions import EvidenceNotFound, EvidenceRequired
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import EvidenceRepository
from ascend.application.policies import AssessmentPolicies
from ascend.domain.assessment import Assessment


class AssessmentService:
    def __init__(
        self,
        evidence_repo: EvidenceRepository,
        event_bus: EventBus,
    ) -> None:
        self._evidence_repo = evidence_repo
        self._event_bus = event_bus

    def complete_assessment(self, command: CompleteAssessment) -> Assessment:
        evidence = self._evidence_repo.get(command.evidence_id)

        decision = AssessmentPolicies.can_complete_assessment(evidence)
        if not decision.is_allowed:
            raise EvidenceRequired(
                f"Policy Violation [{decision.violated_invariant}]: {decision.reason}"
            )

        assessment = Assessment(
            evidence_id=command.evidence_id,
            score=command.score,
            feedback=command.feedback,
            reviewer=command.reviewer,
        )

        if assessment.is_approved:
            evidence.accept()
        else:
            evidence.reject()

        self._evidence_repo.save(evidence)

        return assessment
