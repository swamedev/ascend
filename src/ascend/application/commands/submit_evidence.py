from dataclasses import dataclass

from ascend.domain.evidence import EvidenceType


@dataclass
class SubmitEvidence:
    builder_id: str
    mission_id: str
    artifact: str
    evidence_type: EvidenceType = EvidenceType.DOCUMENT
