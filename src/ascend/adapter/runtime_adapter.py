"""RuntimeAdapter — canonical API for the ASCEND Runtime.

This is the only layer authorized to know both the Python Runtime
and the Canonical Contracts simultaneously. Every method:
  1. Calls the appropriate Runtime service/use case
  2. Transforms the result to canonical dict shapes (mapper.py)
  3. Maps errors to ASCEND_ERROR format (error_mapper.py)
  4. Collects domain events in ARCH-0026 format (event_adapter.py)
"""

from datetime import datetime
from typing import Any

from ascend.adapter.error_mapper import map_error, success_response
from ascend.adapter.event_adapter import to_canonical_envelope
from ascend.adapter.mapper import (
    achievement_to_summary,
    builder_to_canonical,
    competency_to_detail,
    competency_to_summary,
    evidence_to_record,
    journey_to_detail,
    journey_to_summary,
    mission_to_detail,
    mission_to_summary,
)
from ascend.application.commands.complete_assessment import CompleteAssessment
from ascend.application.commands.create_builder import CreateBuilder
from ascend.application.commands.start_mission import StartMission
from ascend.application.commands.submit_evidence import SubmitEvidence
from ascend.application.services.assessment_service import AssessmentService
from ascend.application.services.builder_service import BuilderService
from ascend.application.services.mission_service import MissionService
from ascend.domain.achievement import Achievement
from ascend.domain.evidence import EvidenceType
from ascend.domain.journey import Journey, JourneyStatus
from ascend.domain.mission import Mission
from ascend.infrastructure.events.memory_event_bus import MemoryEventBus
from ascend.infrastructure.persistence.sqlite.builder_repository import (
    SQLiteBuilderRepository,
)
from ascend.infrastructure.persistence.sqlite.connection import ConnectionManager
from ascend.infrastructure.persistence.sqlite.evidence_repository import (
    SQLiteEvidenceRepository,
)
from ascend.infrastructure.persistence.sqlite.migrations import MigrationEngine
from ascend.infrastructure.persistence.sqlite.mission_repository import (
    SQLiteMissionRepository,
)


class RuntimeAdapter:
    """Canonical bridge between the Python Runtime and @ascend/contracts.

    Usage:
        adapter = RuntimeAdapter(db_path=":memory:")
        result = adapter.get_builder("builder-alice")
        if result["success"]:
            print(result["data"])
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn_manager = ConnectionManager(db_path)
        self._event_bus = MemoryEventBus()

        self._builder_repo = SQLiteBuilderRepository(self._conn_manager)
        self._mission_repo = SQLiteMissionRepository(self._conn_manager)
        self._evidence_repo = SQLiteEvidenceRepository(self._conn_manager)

        self._builder_service = BuilderService(
            self._builder_repo, self._event_bus
        )
        self._mission_service = MissionService(
            self._builder_repo,
            self._mission_repo,
            self._evidence_repo,
            self._event_bus,
        )
        self._assessment_service = AssessmentService(
            self._evidence_repo, self._event_bus
        )
        self._migration_engine = MigrationEngine(self._conn_manager)

    @property
    def event_bus(self) -> MemoryEventBus:
        return self._event_bus

    # ------------------------------------------------------------------
    # Builder
    # ------------------------------------------------------------------

    def create_demo_builder(self) -> dict[str, Any]:
        try:
            import uuid
            demo_username = f"Demo_Builder_{uuid.uuid4().hex[:8]}"
            return self.create_builder(username=demo_username, display_name=demo_username)
        except Exception as e:
            return map_error(e)

    def create_builder(
        self, username: str, display_name: str | None = None
    ) -> dict[str, Any]:
        try:
            effective_username = display_name or username
            command = CreateBuilder(username=effective_username)
            dto = self._builder_service.create_builder(command)
            builder = self._builder_repo.get(dto.id)
            if not builder:
                return map_error(
                    Exception(
                        f"Builder '{dto.id}' not found after creation"
                    )
                )
            return success_response(builder_to_canonical(builder))
        except Exception as e:
            return map_error(e)

    def get_builder(self, builder_id: str) -> dict[str, Any]:
        try:
            from ascend.application.exceptions import BuilderNotFound

            try:
                dto = self._builder_service.get_builder(builder_id)
            except BuilderNotFound:
                return success_response(None)
            builder = self._builder_repo.get(dto.id)
            if not builder:
                return success_response(None)
            return success_response(builder_to_canonical(builder))
        except Exception as e:
            return map_error(e)

    def get_builder_by_username(
        self, username: str
    ) -> dict[str, Any]:
        try:
            builder = self._builder_repo.get_by_username(username)
            if not builder:
                return success_response(None)
            return success_response(builder_to_canonical(builder))
        except Exception as e:
            return map_error(e)

    def get_builder_by_id(self, builder_id: str) -> dict[str, Any]:
        return self.get_builder(builder_id)

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------

    def update_profile(
        self, builder_id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            builder = self._builder_repo.get(builder_id)
            if not builder:
                return success_response(None)
            if "name" in updates:
                builder.username = updates["name"]
            self._builder_repo.save(builder)
            self._event_bus.publish(builder.events)
            return success_response(builder_to_canonical(builder))
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Builder list
    # ------------------------------------------------------------------

    def list_builders(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        try:
            builders = self._builder_repo.list(limit=limit, offset=offset)
            total = self._builder_repo.count()
            return success_response(
                [builder_to_canonical(b) for b in builders],
                total=total,
            )
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Journey
    # ------------------------------------------------------------------

    def _fetch_all_missions(self) -> dict[str, Mission]:
        rows = self._conn_manager.get_connection().execute(
            "SELECT id FROM missions"
        ).fetchall()
        ids = [r["id"] for r in rows]
        missions = self._mission_repo.list_by_ids(ids)
        return {m.id: m for m in missions}

    def list_journeys(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        try:
            conn = self._conn_manager.get_connection()
            total = conn.execute("SELECT COUNT(*) as cnt FROM journeys").fetchone()
            total = total["cnt"] if total else 0

            rows = conn.execute(
                "SELECT id, name, description, status FROM journeys ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
            if not rows:
                return success_response([], total=0)

            mission_map = self._fetch_all_missions()
            journeys = []
            for row in rows:
                journey = Journey(
                    name=row["name"],
                    objective=row["description"],
                    status=JourneyStatus(row["status"]),
                    id=row["id"],
                )
                journey.missions = [
                    m for m in mission_map.values()
                ]
                journeys.append(journey)
            return success_response(
                [journey_to_summary(j) for j in journeys],
                total=total,
            )
        except Exception as e:
            return map_error(e)

    def get_journey(self, journey_id: str) -> dict[str, Any]:
        try:
            row = self._conn_manager.get_connection().execute(
                "SELECT id, name, description, status FROM journeys WHERE id = ?",
                (journey_id,),
            ).fetchone()
            if not row:
                return success_response(None)
            journey = Journey(
                name=row["name"],
                objective=row["description"],
                status=JourneyStatus(row["status"]),
                id=row["id"],
            )
            mission_map = self._fetch_all_missions()
            journey.missions = [
                m for m in mission_map.values()
            ]
            return success_response(journey_to_detail(journey))
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Mission
    # ------------------------------------------------------------------

    def list_missions_by_journey(
        self, journey_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            missions = self._mission_repo.list_by_journey(journey_id, limit=limit, offset=offset)
            total = self._mission_repo.count()
            return success_response(
                [mission_to_summary(m) for m in missions],
                total=total,
            )
        except Exception as e:
            return map_error(e)

    def get_mission(self, mission_id: str) -> dict[str, Any]:
        try:
            mission = self._mission_repo.get(mission_id)
            if not mission:
                return success_response(None)
            return success_response(mission_to_detail(mission))
        except Exception as e:
            return map_error(e)

    def start_mission(
        self, builder_id: str, mission_id: str
    ) -> dict[str, Any]:
        try:
            command = StartMission(
                builder_id=builder_id, mission_id=mission_id
            )
            dto = self._mission_service.start_mission(command)
            mission = self._mission_repo.get(dto.id)
            if not mission:
                return map_error(
                    Exception(f"Mission '{dto.id}' not found after start")
                )
            return success_response(mission_to_detail(mission))
        except Exception as e:
            return map_error(e)

    def submit_evidence(
        self,
        builder_id: str,
        mission_id: str,
        artifact: str,
        evidence_type: str = "document",
    ) -> dict[str, Any]:
        try:
            ev_type = EvidenceType(evidence_type)
            command = SubmitEvidence(
                builder_id=builder_id,
                mission_id=mission_id,
                artifact=artifact,
                evidence_type=ev_type,
            )
            dto = self._mission_service.submit_evidence(command)
            evidence = self._evidence_repo.get(dto.id)
            if evidence:
                return success_response(evidence_to_record(evidence))
            return success_response(
                {
                    "id": dto.id,
                    "missionId": mission_id,
                    "builderId": builder_id,
                    "type": evidence_type,
                    "content": artifact,
                    "status": "pending",
                    "submittedAt": dto.submitted_at,
                    "reviewedAt": None,
                    "feedback": None,
                    "competencies": [],
                }
            )
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Evidence
    # ------------------------------------------------------------------

    def list_evidence_by_builder(
        self, builder_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            records = self._evidence_repo.list_by_builder(builder_id, limit=limit, offset=offset)
            total = self._evidence_repo.count_by_builder(builder_id)
            return success_response(
                [evidence_to_record(e) for e in records],
                total=total,
            )
        except Exception as e:
            return map_error(e)

    def get_evidence(self, evidence_id: str) -> dict[str, Any]:
        try:
            evidence = self._evidence_repo.get(evidence_id)
            if not evidence:
                return success_response(None)
            return success_response(evidence_to_record(evidence))
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Assessment
    # ------------------------------------------------------------------

    def complete_assessment(
        self,
        evidence_id: str,
        score: float,
        feedback: str = "",
        reviewer: str = "system",
    ) -> dict[str, Any]:
        try:
            command = CompleteAssessment(
                evidence_id=evidence_id,
                score=score,
                feedback=feedback,
                reviewer=reviewer,
            )
            assessment = self._assessment_service.complete_assessment(
                command
            )
            return success_response(
                {
                    "assessmentId": assessment.id,
                    "title": "Assessment",
                    "score": int(assessment.score * 100),
                    "total": 100,
                    "passed": assessment.is_approved,
                    "attemptsUsed": 1,
                    "completedAt": assessment.created_at.isoformat(),
                    "breakdown": None,
                }
            )
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Competency
    # ------------------------------------------------------------------

    def list_competencies_by_builder(
        self, builder_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            builder = self._builder_repo.get(builder_id)
            if not builder:
                return success_response([], total=0)
            items = builder.competencies[offset:offset + limit]
            total = len(builder.competencies)
            return success_response(
                [competency_to_summary(c) for c in items],
                total=total,
            )
        except Exception as e:
            return map_error(e)

    def get_competency(self, competency_id: str) -> dict[str, Any]:
        try:
            conn = self._conn_manager.get_connection()
            row = conn.execute(
                "SELECT id, name, description, level, criteria FROM competencies WHERE id = ?",
                (competency_id,),
            ).fetchone()
            if not row:
                return success_response(None)
            import json
            comp = type("Comp", (), {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "level": row["level"],
                "criteria": json.loads(row["criteria"]) if row["criteria"] else [],
            })()
            return success_response(competency_to_detail(comp))
        except Exception as e:
            return map_error(e)

    def unlock_competency(
        self,
        builder_id: str,
        name: str,
        description: str = "",
        level: int = 1,
    ) -> dict[str, Any]:
        try:
            from ascend.domain.competency import Competency

            builder = self._builder_repo.get(builder_id)
            if not builder:
                return map_error(
                    Exception(f"Builder '{builder_id}' not found")
                )
            competency = Competency(
                name=name,
                description=description,
                level=level,
                id=f"comp-{name.lower().replace(' ', '-')}",
            )
            builder.add_competency(competency)
            self._builder_repo.save(builder)

            conn = self._conn_manager.get_connection()
            import json
            conn.execute(
                """INSERT OR REPLACE INTO competencies
                   (id, name, description, level, criteria)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    competency.id,
                    competency.name,
                    competency.description,
                    competency.level,
                    json.dumps(competency.criteria),
                ),
            )
            conn.execute(
                """INSERT OR REPLACE INTO builder_competencies
                   (builder_id, competency_id, level, progress, evidence_count)
                   VALUES (?, ?, ?, ?, ?)""",
                (builder_id, competency.id, competency.level, 1.0, 0),
            )
            self._event_bus.publish(builder.events)
            return success_response(builder_to_canonical(builder))
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Achievement
    # ------------------------------------------------------------------

    def list_achievements_by_builder(
        self, builder_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            builder = self._builder_repo.get(builder_id)
            if not builder:
                return success_response([], total=0)
            items = builder.achievements[offset:offset + limit]
            total = len(builder.achievements)
            return success_response(
                [achievement_to_summary(a) for a in items],
                total=total,
            )
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def collect_events(self) -> list[dict[str, Any]]:
        return [
            to_canonical_envelope(evt)
            for evt in self._event_bus.published
        ]

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(self) -> dict[str, Any]:
        return success_response(
            {
                "status": "healthy",
                "version": "0.1.0",
                "uptime": 0,
                "timestamp": datetime.now().isoformat(),
                "checks": {
                    "database": True,
                    "runtime": True,
                    "cache": True,
                },
            }
        )

    # ------------------------------------------------------------------
    # XP
    # ------------------------------------------------------------------

    def award_xp(self, builder_id: str, amount: int) -> dict[str, Any]:
        try:
            self._builder_service.gain_xp(builder_id, amount)
            return success_response(None)
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Mission — mutation helpers
    # ------------------------------------------------------------------

    def mark_mission_completed(self, mission_id: str) -> dict[str, Any]:
        try:
            mission = self._mission_repo.get(mission_id)
            if mission:
                try:
                    mission.complete()
                except ValueError:
                    pass
                self._mission_repo.save(mission)
            return success_response(None)
        except Exception as e:
            return map_error(e)

    def count_completed_missions(self, builder_id: str) -> int:
        try:
            conn = self._conn_manager.get_connection()
            rows = conn.execute(
                "SELECT COUNT(*) as cnt FROM builder_missions WHERE builder_id = ? AND status = ?",
                (builder_id, "completed"),
            ).fetchone()
            return rows["cnt"] if rows else 0
        except Exception:
            return 0

    # ------------------------------------------------------------------
    # Achievement
    # ------------------------------------------------------------------

    def grant_builder_achievement(
        self,
        builder_id: str,
        name: str,
        description: str = "",
        achievement_id: str = "",
    ) -> dict[str, Any]:
        try:
            builder = self._builder_repo.get(builder_id)
            if not builder:
                return map_error(
                    Exception(f"Builder '{builder_id}' not found")
                )
            achievement = Achievement(
                name=name,
                description=description,
                id=achievement_id,
            )
            achievement.earn()
            builder.add_achievement(achievement)
            self._builder_repo.save(builder)

            conn = self._conn_manager.get_connection()
            conn.execute(
                "INSERT OR IGNORE INTO achievements (id, name, description, criteria, badge) VALUES (?, ?, ?, ?, ?)",
                (achievement.id, achievement.name, achievement.description, "[]", ""),
            )
            conn.execute(
                "INSERT OR REPLACE INTO builder_achievements (builder_id, achievement_id, earned_at) VALUES (?, ?, ?)",
                (builder_id, achievement.id, datetime.now().isoformat()),
            )
            return success_response(None)
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Builder — delete
    # ------------------------------------------------------------------

    def delete_builder(self, builder_id: str) -> dict[str, Any]:
        try:
            conn = self._conn_manager.get_connection()
            conn.execute(
                "DELETE FROM builders WHERE id = ?", (builder_id,)
            )
            return success_response(None)
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Journey — seed
    # ------------------------------------------------------------------

    def seed_journeys(self) -> dict[str, Any]:
        try:
            from ascend.package_engine.loader import PackageLoader
            from ascend.runtime.adapters.package_converter import (
                PackageConverter,
            )

            loader = PackageLoader()
            pkg = loader.load_and_validate("packages/python-foundations")
            converter = PackageConverter()
            runtime_pkg = converter.convert(pkg)

            conn = self._conn_manager.get_connection()

            for rj in runtime_pkg.journeys:
                journey = Journey(
                    name=rj.title,
                    objective=rj.description,
                    status=JourneyStatus.AVAILABLE,
                    id=rj.id,
                )
                conn.execute(
                    "INSERT OR REPLACE INTO journeys (id, name, description, status) VALUES (?, ?, ?, ?)",
                    (
                        journey.id,
                        journey.name,
                        journey.objective,
                        journey.status.value,
                    ),
                )

                for rm in rj.missions:
                    difficulty = _parse_difficulty(rm.difficulty)
                    mission = Mission(
                        title=rm.title,
                        objective=rm.description,
                        difficulty=difficulty,
                        xp_reward=rm.xp,
                        id=rm.id,
                    )
                    self._mission_repo.save(mission)

            return self.list_journeys()
        except Exception as e:
            return map_error(e)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._conn_manager.close()

    def initialize_database(self) -> None:
        engine = MigrationEngine(self._conn_manager)
        engine.apply_all()


def _parse_difficulty(difficulty: str) -> int:
    mapping = {"beginner": 1, "intermediate": 2, "advanced": 3}
    return mapping.get(difficulty, 1)
