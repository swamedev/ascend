from uuid import UUID

import pytest

from ascend.cognitive.collector import EVENT_TYPE_MAP, ObservationCollector
from ascend.cognitive.models import (
    InMemoryObservationStore,
    Observation,
)
from ascend.domain.events import (
    AchievementEarned,
    AssessmentCompleted,
    BuilderCreated,
    CompetencyUnlocked,
    DomainEvent,
    EventType,
    EvidenceSubmitted,
    MissionStarted,
)
from ascend.infrastructure.events.memory_event_bus import MemoryEventBus


# ---------------------------------------------------------------------------
# Observation model
# ---------------------------------------------------------------------------


class TestObservationModel:
    def test_observation_creation(self):
        obs = Observation(
            id="obs-001",
            type="mission.completed",
            source="runtime",
            timestamp="2026-07-21T14:30:00Z",
            data={"missionId": "m-1", "score": 85},
            context={"builderId": "bld-42", "missionId": "m-1"},
            metadata={"observationSchema": "1.0", "collector": "test"},
        )
        assert obs.id == "obs-001"
        assert obs.type == "mission.completed"
        assert obs.source == "runtime"
        assert obs.data["missionId"] == "m-1"
        assert obs.context["builderId"] == "bld-42"

    def test_observation_default_metadata(self):
        obs = Observation(
            id="obs-002",
            type="evidence.submitted",
            source="builder",
            timestamp="2026-07-21T15:00:00Z",
            data={},
            context={"builderId": "bld-1"},
        )
        assert obs.metadata == {}


# ---------------------------------------------------------------------------
# InMemoryObservationStore
# ---------------------------------------------------------------------------


class TestInMemoryObservationStore:
    @pytest.fixture
    def store(self):
        return InMemoryObservationStore()

    @pytest.fixture
    def sample_observations(self):
        return [
            Observation(
                id="o-1",
                type="builder.created",
                source="runtime",
                timestamp="2026-07-21T10:00:00Z",
                data={},
                context={"builderId": "bld-a"},
                metadata={},
            ),
            Observation(
                id="o-2",
                type="mission.started",
                source="runtime",
                timestamp="2026-07-21T10:05:00Z",
                data={},
                context={"builderId": "bld-a", "missionId": "m-1"},
                metadata={},
            ),
            Observation(
                id="o-3",
                type="builder.created",
                source="runtime",
                timestamp="2026-07-21T11:00:00Z",
                data={},
                context={"builderId": "bld-b"},
                metadata={},
            ),
        ]

    def test_save_and_count(self, store, sample_observations):
        for obs in sample_observations:
            store.save(obs)
        assert store.count_all() == 3

    def test_list_all(self, store, sample_observations):
        for obs in sample_observations:
            store.save(obs)
        result = store.list_all()
        assert len(result) == 3
        assert result[0].id == "o-1"
        assert result[2].id == "o-3"

    def test_list_by_builder(self, store, sample_observations):
        for obs in sample_observations:
            store.save(obs)
        result = store.list_by_builder("bld-a")
        assert len(result) == 2
        assert all(o.context["builderId"] == "bld-a" for o in result)

    def test_count_by_builder(self, store, sample_observations):
        for obs in sample_observations:
            store.save(obs)
        assert store.count_by_builder("bld-a") == 2
        assert store.count_by_builder("bld-b") == 1
        assert store.count_by_builder("bld-none") == 0

    def test_pagination(self, store):
        for i in range(10):
            store.save(
                Observation(
                    id=f"o-{i}",
                    type="test",
                    source="runtime",
                    timestamp="2026-07-21T00:00:00Z",
                    data={},
                    context={"builderId": "bld-a"},
                    metadata={},
                )
            )
        assert len(store.list_all(limit=3, offset=0)) == 3
        assert len(store.list_all(limit=3, offset=3)) == 3
        assert len(store.list_all(limit=3, offset=9)) == 1
        assert len(store.list_all(limit=10, offset=20)) == 0

    def test_list_by_builder_pagination(self, store):
        for i in range(5):
            store.save(
                Observation(
                    id=f"a-{i}",
                    type="test",
                    source="runtime",
                    timestamp="2026-07-21T00:00:00Z",
                    data={},
                    context={"builderId": "bld-a"},
                    metadata={},
                )
            )
        for i in range(5):
            store.save(
                Observation(
                    id=f"b-{i}",
                    type="test",
                    source="runtime",
                    timestamp="2026-07-21T00:00:00Z",
                    data={},
                    context={"builderId": "bld-b"},
                    metadata={},
                )
            )
        result = store.list_by_builder("bld-a", limit=2, offset=1)
        assert len(result) == 2
        assert result[0].id == "a-1"
        assert result[1].id == "a-2"

    def test_empty_store(self, store):
        assert store.count_all() == 0
        assert store.list_all() == []
        assert store.list_by_builder("any") == []


# ---------------------------------------------------------------------------
# ObservationCollector — event mapping and subscription
# ---------------------------------------------------------------------------


class TestObservationCollectorEventMapping:
    @pytest.fixture
    def store(self):
        return InMemoryObservationStore()

    @pytest.fixture
    def event_bus(self):
        return MemoryEventBus()

    @pytest.fixture
    def collector(self, event_bus, store):
        return ObservationCollector(event_bus=event_bus, store=store)

    def test_subscribes_to_all_event_types(self, event_bus, store, collector):
        assert len(event_bus._subscribers) == len(EventType)
        for event_type in EventType:
            assert event_type.value in event_bus._subscribers
            assert len(event_bus._subscribers[event_type.value]) == 1

    def test_collector_property(self, collector, store):
        assert collector.store is store

    def test_converts_builder_created_event(self, event_bus, store, collector):
        event = BuilderCreated("bld-1", "Alice")
        event_bus.publish([event])
        assert store.count_all() == 1
        obs = store.list_all()[0]
        assert obs.type == EVENT_TYPE_MAP[EventType.BUILDER_CREATED]
        assert obs.source == "runtime"
        assert obs.context["builderId"] == "bld-1"
        assert obs.data["username"] == "Alice"
        assert obs.metadata["collector"] == "observation-collector"
        assert UUID(obs.id)

    def test_converts_mission_started_event(self, event_bus, store, collector):
        event = MissionStarted("m-1", "bld-1")
        event_bus.publish([event])
        obs = store.list_all()[0]
        assert obs.type == EVENT_TYPE_MAP[EventType.MISSION_STARTED]
        assert obs.context["builderId"] == "bld-1"
        assert obs.context["missionId"] == "m-1"

    def test_converts_evidence_submitted_event(self, event_bus, store, collector):
        event = EvidenceSubmitted("ev-1", "m-1", "bld-1")
        event_bus.publish([event])
        obs = store.list_all()[0]
        assert obs.type == EVENT_TYPE_MAP[EventType.EVIDENCE_SUBMITTED]
        assert obs.context["builderId"] == "bld-1"
        assert obs.context["missionId"] == "m-1"
        assert obs.context["evidenceId"] == "ev-1"

    def test_converts_assessment_completed_event(self, event_bus, store, collector):
        event = AssessmentCompleted("a-1", "ev-1", 0.85)
        event_bus.publish([event])
        obs = store.list_all()[0]
        assert obs.type == EVENT_TYPE_MAP[EventType.ASSESSMENT_COMPLETED]
        assert obs.data["score"] == 0.85

    def test_converts_competency_unlocked_event(self, event_bus, store, collector):
        event = CompetencyUnlocked("c-1", "bld-1", 2)
        event_bus.publish([event])
        obs = store.list_all()[0]
        assert obs.type == EVENT_TYPE_MAP[EventType.COMPETENCY_UNLOCKED]
        assert obs.context["builderId"] == "bld-1"
        assert obs.data["level"] == 2

    def test_converts_achievement_earned_event(self, event_bus, store, collector):
        event = AchievementEarned("ach-1", "bld-1")
        event_bus.publish([event])
        obs = store.list_all()[0]
        assert obs.type == EVENT_TYPE_MAP[EventType.ACHIEVEMENT_EARNED]
        assert obs.context["builderId"] == "bld-1"

    def test_multiple_events_accumulate(self, event_bus, store, collector):
        event_bus.publish([BuilderCreated("bld-1", "Alice")])
        event_bus.publish([MissionStarted("m-1", "bld-1")])
        event_bus.publish([MissionStarted("m-2", "bld-1")])
        assert store.count_all() == 3
        assert store.count_by_builder("bld-1") == 3

    def test_events_from_different_builders(self, event_bus, store, collector):
        event_bus.publish([BuilderCreated("bld-a", "Alice")])
        event_bus.publish([BuilderCreated("bld-b", "Bob")])
        assert store.count_by_builder("bld-a") == 1
        assert store.count_by_builder("bld-b") == 1

    def test_event_has_valid_uuid(self, event_bus, store, collector):
        event_bus.publish([BuilderCreated("bld-1", "Alice")])
        obs = store.list_all()[0]
        parsed = UUID(obs.id)
        assert parsed.version == 4

    def test_event_timestamp_is_iso_format(self, event_bus, store, collector):
        event = BuilderCreated("bld-1", "Alice")
        event_bus.publish([event])
        obs = store.list_all()[0]
        assert "T" in obs.timestamp
        assert obs.timestamp.endswith("Z") or "+" in obs.timestamp or obs.timestamp.count("-") >= 2


# ---------------------------------------------------------------------------
# ObservationCollector — integration with RuntimeAdapter
# ---------------------------------------------------------------------------


class TestObservationCollectorIntegration:
    @pytest.fixture
    def adapter(self):
        from ascend.adapter.runtime_adapter import RuntimeAdapter

        a = RuntimeAdapter(db_path=":memory:")
        a.initialize_database()
        return a

    @pytest.fixture
    def store(self):
        return InMemoryObservationStore()

    def test_collects_events_via_adapter(self, adapter, store):
        collector = ObservationCollector(
            event_bus=adapter.event_bus, store=store
        )
        adapter.create_builder("Alice")
        adapter.create_builder("Bob")
        assert store.count_all() == 2
        assert store.count_by_builder("builder-alice") == 1
        assert store.count_by_builder("builder-bob") == 1

    def test_collector_does_not_affect_adapter(self, adapter, store):
        collector = ObservationCollector(
            event_bus=adapter.event_bus, store=store
        )
        adapter.create_builder("Alice")
        result = adapter.get_builder("builder-alice")
        assert result["success"] is True
        assert result["data"]["profile"]["name"] == "Alice"

    def test_multiple_operations(self, adapter, store):
        collector = ObservationCollector(
            event_bus=adapter.event_bus, store=store
        )
        adapter.create_builder("Charlie")
        adapter.seed_journeys()
        assert store.count_all() > 0


# ---------------------------------------------------------------------------
# EVENT_TYPE_MAP completeness
# ---------------------------------------------------------------------------


class TestEventTypeMap:
    def test_all_event_types_mapped(self):
        mapped_types = set(EVENT_TYPE_MAP.keys())
        all_types = set(EventType)
        assert mapped_types == all_types, (
            f"Missing mappings: {all_types - mapped_types}"
        )

    def test_all_mapped_types_are_strings(self):
        for event_type, obs_type in EVENT_TYPE_MAP.items():
            assert isinstance(obs_type, str)
            assert "." in obs_type, (
                f"Observation type '{obs_type}' should use dot notation"
            )
