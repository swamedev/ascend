from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ascend.domain.evidence import Evidence, EvidenceStatus


class PolicyDecisionStatus(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class PolicyDecision:
    status: PolicyDecisionStatus
    reason: str
    violated_invariant: Optional[str] = None
    severity: str = "CRITICAL"

    @property
    def is_allowed(self) -> bool:
        return self.status == PolicyDecisionStatus.ALLOW


class CompetencyPolicies:
    @staticmethod
    def can_unlock_competency(evidence: Optional[Evidence]) -> PolicyDecision:
        if not evidence:
            return PolicyDecision(
                status=PolicyDecisionStatus.DENY,
                reason="Unlock denied: No evidence provided.",
                violated_invariant="I2",
            )

        if evidence.status != EvidenceStatus.ACCEPTED:
            return PolicyDecision(
                status=PolicyDecisionStatus.DENY,
                reason=f"Unlock denied: Evidence must be ACCEPTED. Current status is {evidence.status.value}.",
                violated_invariant="I2",
            )

        return PolicyDecision(
            status=PolicyDecisionStatus.ALLOW,
            reason="Evidence is valid and accepted. Competency unlock authorized.",
        )


class AssessmentPolicies:
    @staticmethod
    def can_complete_assessment(evidence: Optional[Evidence]) -> PolicyDecision:
        if not evidence:
            return PolicyDecision(
                status=PolicyDecisionStatus.DENY,
                reason="Assessment denied: Evidence not found.",
                violated_invariant="I2",
            )

        if evidence.status == EvidenceStatus.ACCEPTED or evidence.status == EvidenceStatus.REJECTED:
            return PolicyDecision(
                status=PolicyDecisionStatus.DENY,
                reason=f"Assessment denied: Evidence is already {evidence.status.value}.",
                violated_invariant="StateProtocol",
            )

        return PolicyDecision(
            status=PolicyDecisionStatus.ALLOW,
            reason="Evidence is pending review. Assessment authorized.",
        )
