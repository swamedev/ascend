from ascend.domain.mission import Mission, MissionStatus

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteMissionRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

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
        mission = Mission(
            title=row["title"],
            objective=row["objective"],
            difficulty=row["difficulty"],
            xp_reward=row["xp_reward"],
            id=row["id"],
            status=MissionStatus(row["status"]),
        )
        return mission

    def list_by_journey(self, journey_id: str) -> list[Mission]:
        rows = self._fetch_all(
            "SELECT id FROM missions"
        )
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]
