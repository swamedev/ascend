from datetime import datetime

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

    def _row_to_evidence(self, row: dict) -> Evidence:
        evidence = Evidence(
            artifact=row["artifact"],
            type=EvidenceType(row["type"]),
            id=row["id"],
            builder_id=row["builder_id"],
            mission_id=row["mission_id"],
            status=EvidenceStatus(row["status"]),
        )
        if row["submitted_at"]:
            evidence.submitted_at = datetime.fromisoformat(row["submitted_at"])
        return evidence

    def get(self, evidence_id: str) -> Evidence | None:
        row = self._fetch_one(
            "SELECT id, builder_id, mission_id, artifact, type, status, submitted_at FROM evidence WHERE id = ?",
            (evidence_id,),
        )
        if not row:
            return None
        return self._row_to_evidence(row)

    def list_by_builder(self, builder_id: str, limit: int = 50, offset: int = 0) -> list[Evidence]:
        rows = self._fetch_all(
            "SELECT id, builder_id, mission_id, artifact, type, status, submitted_at FROM evidence WHERE builder_id = ? ORDER BY submitted_at DESC LIMIT ? OFFSET ?",
            (builder_id, limit, offset),
        )
        return [self._row_to_evidence(r) for r in rows]

    def list_by_builder_and_mission(self, builder_id: str, mission_id: str) -> list[Evidence]:
        rows = self._fetch_all(
            "SELECT id, builder_id, mission_id, artifact, type, status, submitted_at FROM evidence WHERE builder_id = ? AND mission_id = ?",
            (builder_id, mission_id),
        )
        return [self._row_to_evidence(r) for r in rows]

    def count_by_builder(self, builder_id: str) -> int:
        row = self._fetch_one(
            "SELECT COUNT(*) as cnt FROM evidence WHERE builder_id = ?",
            (builder_id,),
        )
        return row["cnt"] if row else 0
