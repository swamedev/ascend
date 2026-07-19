import json

from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.achievement import Achievement

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteBuilderRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def save(self, builder: Builder) -> None:
        self._execute(
            """INSERT OR REPLACE INTO builders (id, username, level, xp)
               VALUES (?, ?, ?, ?)""",
            (builder.id, builder.username, builder.level, builder.xp),
        )
        for comp in builder.competencies:
            self._execute(
                """INSERT OR REPLACE INTO competencies (id, name, description, level, criteria)
                   VALUES (?, ?, ?, ?, ?)""",
                (comp.id, comp.name, comp.description, comp.level, json.dumps(comp.criteria)),
            )
            self._execute(
                """INSERT OR REPLACE INTO builder_competencies (builder_id, competency_id, level, progress, evidence_count)
                   VALUES (?, ?, ?, ?, ?)""",
                (builder.id, comp.id, comp.level, 1.0 if comp.criteria else 0.0, 0),
            )
        for ach in builder.achievements:
            self._execute(
                """INSERT OR IGNORE INTO achievements (id, name, description, criteria)
                   VALUES (?, ?, ?, ?)""",
                (ach.id, ach.name, ach.description, json.dumps(ach.criteria)),
            )
            self._execute(
                """INSERT OR REPLACE INTO builder_achievements (builder_id, achievement_id, earned_at)
                   VALUES (?, ?, ?)""",
                (
                    builder.id,
                    ach.id,
                    ach.earned_at.isoformat() if ach.earned_at else None,
                ),
            )

    def get(self, builder_id: str) -> Builder | None:
        row = self._fetch_one(
            "SELECT id, username, level, xp FROM builders WHERE id = ?",
            (builder_id,),
        )
        if not row:
            return None

        builder = Builder(
            username=row["username"],
            id=row["id"],
            level=row["level"],
            xp=row["xp"],
        )
        builder.events.clear()

        ach_rows = self._fetch_all(
            """SELECT a.id, a.name, a.description, a.criteria, ba.earned_at
               FROM achievements a
               JOIN builder_achievements ba ON ba.achievement_id = a.id
               WHERE ba.builder_id = ?""",
            (builder_id,),
        )
        for ar in ach_rows:
            ach = Achievement(
                name=ar["name"],
                description=ar["description"],
                criteria=json.loads(ar["criteria"]) if ar["criteria"] else [],
                id=ar["id"],
            )
            if ar["earned_at"]:
                ach.earned_at = ar["earned_at"]
            builder.add_achievement(ach)

        comp_rows = self._fetch_all(
            """SELECT c.id, c.name, c.description, c.level, c.criteria
               FROM competencies c
               JOIN builder_competencies bc ON bc.competency_id = c.id
               WHERE bc.builder_id = ?""",
            (builder_id,),
        )
        for cr in comp_rows:
            comp = Competency(
                name=cr["name"],
                description=cr["description"],
                level=cr["level"],
                criteria=json.loads(cr["criteria"]) if cr["criteria"] else [],
                id=cr["id"],
            )
            builder.add_competency(comp)

        return builder

    def get_by_username(self, username: str) -> Builder | None:
        row = self._fetch_one(
            "SELECT id FROM builders WHERE username = ?",
            (username,),
        )
        if not row:
            return None
        return self.get(row["id"])

    def list(self) -> list[Builder]:
        rows = self._fetch_all("SELECT id FROM builders")
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]
