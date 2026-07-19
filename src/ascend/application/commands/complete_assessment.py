from dataclasses import dataclass


@dataclass
class CompleteAssessment:
    evidence_id: str
    score: float
    feedback: str = ""
    reviewer: str = ""
