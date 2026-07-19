from ascend.domain.evidence import Evidence, EvidenceStatus, EvidenceType

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteEvidenceRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def save(self, evidence: Evidence) -> None:
        self._execute(
            """INSERT OR REPLACE INTO evidence (id, builder_id, mission_id, artifact, type, status, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                evidence.id,
                evidence.builder_id,
                evidence.mission_id,
                evidence.artifact,
                evidence.type.value,
                evidence.status.value,
                evidence.submitted_at.isoformat() if evidence.submitted_at else None,
            ),
        )

    def get(self, evidence_id: str) -> Evidence | None:
        row = self._fetch_one(
            "SELECT id, builder_id, mission_id, artifact, type, status, submitted_at FROM evidence WHERE id = ?",
            (evidence_id,),
        )
        if not row:
            return None
        evidence = Evidence(
            artifact=row["artifact"],
            type=EvidenceType(row["type"]),
            id=row["id"],
            builder_id=row["builder_id"],
            mission_id=row["mission_id"],
            status=EvidenceStatus(row["status"]),
        )
        if row["submitted_at"]:
            from datetime import datetime
            evidence.submitted_at = datetime.fromisoformat(row["submitted_at"])
        return evidence

    def list_by_builder(self, builder_id: str) -> list[Evidence]:
        rows = self._fetch_all(
            "SELECT id FROM evidence WHERE builder_id = ?",
            (builder_id,),
        )
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]
