from dataclasses import dataclass


@dataclass
class EvidenceDTO:
    id: str
    artifact: str
    type: str
    status: str
    builder_id: str
    submitted_at: str = ""
