from ascend.domain.mission import Mission, MissionStatus

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteMissionRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def _row_to_mission(self, row: dict) -> Mission:
        return Mission(
            title=row["title"],
            objective=row["objective"],
            difficulty=row["difficulty"],
            xp_reward=row["xp_reward"],
            id=row["id"],
            status=MissionStatus(row["status"]),
        )

    def save(self, mission: Mission) -> None:
        self._execute(
            """INSERT OR REPLACE INTO missions (id, title, objective, difficulty, xp_reward, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                mission.id,
                mission.title,
                mission.objective,
                mission.difficulty,
                mission.xp_reward,
                mission.status.value,
            ),
        )

    def get(self, mission_id: str) -> Mission | None:
        row = self._fetch_one(
            "SELECT id, title, objective, difficulty, xp_reward, status FROM missions WHERE id = ?",
            (mission_id,),
        )
        if not row:
            return None
        return self._row_to_mission(row)

    def list_by_ids(self, mission_ids: list[str]) -> list[Mission]:
        if not mission_ids:
            return []
        placeholders = ",".join("?" for _ in mission_ids)
        rows = self._fetch_all(
            f"SELECT id, title, objective, difficulty, xp_reward, status FROM missions WHERE id IN ({placeholders})",
            tuple(mission_ids),
        )
        return [self._row_to_mission(r) for r in rows]

    def list_by_journey(self, journey_id: str, limit: int = 50, offset: int = 0) -> list[Mission]:
        rows = self._fetch_all(
            "SELECT id FROM missions ORDER BY id LIMIT ? OFFSET ?",
            (limit, offset),
        )
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]

    def count(self) -> int:
        row = self._fetch_one("SELECT COUNT(*) as cnt FROM missions")
        return row["cnt"] if row else 0
