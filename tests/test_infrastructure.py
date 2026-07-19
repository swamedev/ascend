import pytest

from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.mission import Mission, MissionStatus
from ascend.domain.evidence import Evidence, EvidenceType
from ascend.domain.achievement import Achievement
from ascend.domain.events import BuilderCreated

from ascend.infrastructure.persistence.sqlite.connection import ConnectionManager
from ascend.infrastructure.persistence.sqlite.builder_repository import (
    SQLiteBuilderRepository,
)
from ascend.infrastructure.persistence.sqlite.mission_repository import (
    SQLiteMissionRepository,
)
from ascend.infrastructure.persistence.sqlite.evidence_repository import (
    SQLiteEvidenceRepository,
)
from ascend.infrastructure.persistence.sqlite.event_store import SQliteEventStore
from ascend.infrastructure.persistence.sqlite.migrations import MigrationEngine
from ascend.infrastructure.events.memory_event_bus import MemoryEventBus
from ascend.infrastructure.uow import UnitOfWork


@pytest.fixture
def conn_manager():
    cm = ConnectionManager(":memory:")
    MigrationEngine(cm).apply_all()
    yield cm
    cm.close()


@pytest.fixture
def builder_repo(conn_manager):
    return SQLiteBuilderRepository(conn_manager)


@pytest.fixture
def mission_repo(conn_manager):
    return SQLiteMissionRepository(conn_manager)


@pytest.fixture
def evidence_repo(conn_manager):
    return SQLiteEvidenceRepository(conn_manager)


@pytest.fixture
def event_store(conn_manager):
    return SQliteEventStore(conn_manager)


@pytest.fixture
def event_bus():
    return MemoryEventBus()


@pytest.fixture
def uow(conn_manager):
    return UnitOfWork(conn_manager)


class TestSQLiteConnection:
    def test_creates_tables(self, conn_manager):
        tables = conn_manager.get_connection().execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        names = [t["name"] for t in tables]
        assert "builders" in names
        assert "missions" in names
        assert "evidence" in names
        assert "events" in names

    def test_memory_database(self, conn_manager):
        conn = conn_manager.get_connection()
        conn.execute("INSERT INTO builders (id, username) VALUES ('b1', 'test')")
        row = conn.execute(
            "SELECT username FROM builders WHERE id = ?", ("b1",)
        ).fetchone()
        assert row["username"] == "test"


class TestBuilderRepository:
    def test_save_and_get_builder(self, builder_repo):
        builder = Builder("Alex")
        builder.gain_xp(500)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == "Alex"
        assert loaded.level == 2
        assert loaded.xp == 500

    def test_get_nonexistent_builder(self, builder_repo):
        loaded = builder_repo.get("nonexistent")
        assert loaded is None

    def test_save_builder_with_competency(self, builder_repo):
        builder = Builder("Maria")
        comp = Competency("Linux", "Linux admin", level=2)
        builder.add_competency(comp)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert len(loaded.competencies) == 1
        assert loaded.competencies[0].name == "Linux"
        assert loaded.competencies[0].level == 2

    def test_save_builder_with_achievement(self, builder_repo):
        builder = Builder("Joao")
        ach = Achievement("First Mission")
        ach.earn()
        builder.add_achievement(ach)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert len(loaded.achievements) == 1

    def test_update_builder(self, builder_repo):
        builder = Builder("Ana")
        builder_repo.save(builder)
        builder.gain_xp(1000)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded.xp == 1000
        assert loaded.level == 3

    def test_get_by_username(self, builder_repo):
        builder = Builder("Carlos")
        builder_repo.save(builder)

        loaded = builder_repo.get_by_username("Carlos")
        assert loaded is not None
        assert loaded.id == builder.id

    def test_list_builders(self, builder_repo):
        builder_repo.save(Builder("A"))
        builder_repo.save(Builder("B"))
        builder_repo.save(Builder("C"))

        all_builders = builder_repo.list()
        assert len(all_builders) == 3


class TestMissionRepository:
    def test_save_and_get_mission(self, mission_repo):
        mission = Mission("Linux Explorer", "Navigate Linux")
        mission_repo.save(mission)

        loaded = mission_repo.get(mission.id)
        assert loaded is not None
        assert loaded.title == "Linux Explorer"
        assert loaded.status == MissionStatus.AVAILABLE

    def test_update_mission_status(self, mission_repo):
        mission = Mission("Docker")
        mission_repo.save(mission)
        mission.start()
        mission_repo.save(mission)

        loaded = mission_repo.get(mission.id)
        assert loaded.status == MissionStatus.STARTED


class TestEvidenceRepository:
    def test_save_and_get_evidence(self, conn_manager, evidence_repo):
        conn = conn_manager.get_connection()
        conn.execute(
            "INSERT INTO builders (id, username) VALUES (?, ?)",
            ("builder-1", "TestBuilder"),
        )
        conn.execute(
            "INSERT INTO missions (id, title) VALUES (?, ?)",
            ("mission-1", "TestMission"),
        )
        evidence = Evidence("report.pdf", EvidenceType.DOCUMENT)
        evidence.submit("builder-1")
        evidence.mission_id = "mission-1"
        evidence_repo.save(evidence)

        loaded = evidence_repo.get(evidence.id)
        assert loaded is not None
        assert loaded.artifact == "report.pdf"
        assert loaded.status.value == "submitted"

    def test_list_by_builder(self, conn_manager, evidence_repo):
        conn = conn_manager.get_connection()
        conn.execute(
            "INSERT INTO builders (id, username) VALUES (?, ?)", ("b1", "B1")
        )
        conn.execute(
            "INSERT INTO builders (id, username) VALUES (?, ?)", ("b2", "B2")
        )
        conn.execute(
            "INSERT INTO missions (id, title) VALUES (?, ?)", ("m1", "M1")
        )
        e1 = Evidence("f1")
        e1.submit("b1")
        e1.mission_id = "m1"
        e2 = Evidence("f2")
        e2.submit("b1")
        e2.mission_id = "m1"
        e3 = Evidence("f3")
        e3.submit("b2")
        e3.mission_id = "m1"
        evidence_repo.save(e1)
        evidence_repo.save(e2)
        evidence_repo.save(e3)

        b1_evidence = evidence_repo.list_by_builder("b1")
        assert len(b1_evidence) == 2


class TestEventStore:
    def test_append_event(self, event_store, builder_repo):
        builder = Builder("Alex")
        builder_repo.save(builder)

        for event in builder.events:
            event_store.append(event)

        stored = event_store.list_all()
        assert len(stored) >= 1
        assert stored[0]["event_type"] == "builder_created"

    def test_get_by_aggregate(self, event_store):
        from ascend.domain.events import BuilderCreated

        event = BuilderCreated("b1", "Alex")
        event_store.append(event)

        results = event_store.get_by_aggregate("b1")
        assert len(results) == 1


class TestUnitOfWork:
    def test_commit_persists_data(self, conn_manager, builder_repo, uow):
        with uow:
            builder = Builder("UoW Test")
            builder_repo.save(builder)
            uow.commit()

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == "UoW Test"

    def test_rollback_undoes_changes(self, conn_manager, builder_repo, uow):
        builder = Builder("Rollback Test")
        try:
            with uow:
                builder_repo.save(builder)
                raise ValueError("force rollback")
        except ValueError:
            pass

        loaded = builder_repo.get(builder.id)
        assert loaded is None

    def test_rollback_on_exception(self, conn_manager, builder_repo, uow):
        try:
            with uow:
                builder_repo.save(Builder("Fail"))
                raise RuntimeError("fail")
        except RuntimeError:
            pass

        loaded = builder_repo.get_by_username("Fail")
        assert loaded is None


class TestMemoryEventBus:
    def test_publish_events(self, event_bus):
        builder = Builder("Alex")
        event_bus.publish(builder.events)

        assert len(event_bus.published) == 1
        assert event_bus.published[0].event_type.value == "builder_created"

    def test_subscribe_and_notify(self, event_bus):
        received = []

        def handler(event):
            received.append(event)

        event_bus.subscribe("builder_created", handler)
        builder = Builder("Maria")
        event_bus.publish(builder.events)

        assert len(received) == 1

    def test_clear(self, event_bus):
        builder = Builder("Test")
        event_bus.publish(builder.events)
        event_bus.clear()
        assert len(event_bus.published) == 0


class TestFullPersistenceFlow:
    def test_persist_and_retrieve_builder(self, builder_repo, event_store):
        builder = Builder("Alex")
        builder.gain_xp(750)
        comp = Competency("Linux", level=2)
        builder.add_competency(comp)
        ach = Achievement("First Steps")
        ach.earn()
        builder.add_achievement(ach)

        builder_repo.save(builder)
        for event in builder.events:
            event_store.append(event)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == "Alex"
        assert loaded.xp == 750
        assert loaded.level == 2
        assert len(loaded.competencies) == 1
        assert len(loaded.achievements) == 1

        stored_events = event_store.list_all()
        assert len(stored_events) == 1
        assert stored_events[0]["aggregate_id"] == builder.id

    def test_architect_goal(self, builder_repo):
        """
        Meta do Sprint 3 (Chief Architect):
        "Ao final do Sprint 3 quero conseguir executar algo assim:
         builder = CreateBuilder.execute(...)
         repo.save(builder)
         loaded = repo.get(builder.id)
         assert loaded.username == builder.username"
        """
        builder = Builder("ChiefArchitect")
        builder_repo.save(builder)
        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == builder.username
        assert loaded.xp == builder.xp
        assert loaded.level == builder.level
