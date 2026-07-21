import pytest

from ascend.cognitive import (
    CompositeExtractor,
    DirectExtractor,
    InMemorySignalStore,
    NormalizedObservation,
    Signal,
    SignalExtractor,
    SignalType,
    confidence_decay,
)


def _make_obs(
    obs_type: str,
    data: dict | None = None,
    context: dict | None = None,
    obs_id: str | None = None,
) -> NormalizedObservation:
    return NormalizedObservation(
        id=obs_id or "obs-1",
        type=obs_type,
        source="test",
        timestamp="2026-07-21T12:00:00Z",
        data=data or {},
        context=context or {"builderId": "builder-1"},
        metadata={},
        trace={"correlationId": "corr-1", "causationId": None},
    )


def _ulid_counter() -> str:
    _ulid_counter.idx += 1
    return f"ulid-{_ulid_counter.idx:04d}"
_ulid_counter.idx = 0


def _reset_counter() -> None:
    _ulid_counter.idx = 0


# --- Signal Model ------------------------------------------------------------


class TestSignalModel:
    def test_creates_signal(self):
        s = Signal(
            id="sig-1",
            observationId="obs-1",
            type=SignalType.XP_GAINED.value,
            value=150,
            confidence=1.0,
            extractedAt="2026-07-21T12:00:00Z",
        )
        assert s.id == "sig-1"
        assert s.observationId == "obs-1"
        assert s.type == "xp_gained"
        assert s.value == 150
        assert s.confidence == 1.0
        assert s.metadata == {}

    def test_signal_with_metadata(self):
        s = Signal(
            id="sig-1",
            observationId="obs-1",
            type=SignalType.COMPLETION_RATE.value,
            value=0.85,
            confidence=1.0,
            extractedAt="2026-07-21T12:00:00Z",
            metadata={"ruleName": "CompletionRateRule", "builderId": "builder-1"},
        )
        assert s.metadata["ruleName"] == "CompletionRateRule"
        assert s.metadata["builderId"] == "builder-1"


# --- SignalType Enum ---------------------------------------------------------


class TestSignalType:
    def test_all_types_have_values(self):
        for t in SignalType:
            assert isinstance(t.value, str)
            assert len(t.value) > 0

    def test_progress_types(self):
        assert SignalType.XP_GAINED.value == "xp_gained"
        assert SignalType.COMPLETION_RATE.value == "completion_rate"
        assert SignalType.TIME_SPENT.value == "time_spent"
        assert SignalType.SCORE_ACHIEVED.value == "score_achieved"

    def test_composite_types(self):
        assert SignalType.ROLLING_COMPLETION_RATE.value == "rolling_completion_rate"
        assert SignalType.ROLLING_AVG_XP.value == "rolling_avg_xp"
        assert SignalType.STREAK_ACTIVE.value == "streak_active"

    def test_twenty_two_types_defined(self):
        assert len(SignalType) == 22


# --- InMemorySignalStore -----------------------------------------------------


class TestInMemorySignalStore:
    def make_store(self) -> InMemorySignalStore:
        return InMemorySignalStore()

    def make_signal(self, obs_id="obs-1", sig_type="xp_gained",
                    value=150.0, builder="b-1") -> Signal:
        return Signal(
            id=f"sig-{obs_id}-{sig_type}",
            observationId=obs_id,
            type=sig_type,
            value=value,
            confidence=1.0,
            extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": builder},
        )

    def test_save_and_count(self):
        store = self.make_store()
        store.save(self.make_signal())
        assert store.count_all() == 1

    def test_save_many(self):
        store = self.make_store()
        sigs = [self.make_signal(obs_id=f"obs-{i}") for i in range(5)]
        store.save_many(sigs)
        assert store.count_all() == 5

    def test_get_by_observation(self):
        store = self.make_store()
        store.save(self.make_signal(obs_id="obs-a"))
        store.save(self.make_signal(obs_id="obs-b"))
        store.save(self.make_signal(obs_id="obs-a", sig_type="completion_rate"))
        results = store.get_by_observation("obs-a")
        assert len(results) == 2
        assert all(s.observationId == "obs-a" for s in results)

    def test_list_by_builder(self):
        store = self.make_store()
        store.save(self.make_signal(obs_id="o1", builder="b-1"))
        store.save(self.make_signal(obs_id="o2", builder="b-1"))
        store.save(self.make_signal(obs_id="o3", builder="b-2"))
        results = store.list_by_builder("b-1")
        assert len(results) == 2

    def test_list_by_builder_with_type_filter(self):
        store = self.make_store()
        store.save(self.make_signal(obs_id="o1", builder="b-1", sig_type="xp_gained"))
        store.save(self.make_signal(obs_id="o2", builder="b-1", sig_type="completion_rate"))
        store.save(self.make_signal(obs_id="o3", builder="b-1", sig_type="xp_gained"))
        results = store.list_by_builder("b-1", signal_type="xp_gained")
        assert len(results) == 2

    def test_list_recent_returns_last_n(self):
        store = self.make_store()
        for i in range(20):
            store.save(self.make_signal(obs_id=f"obs-{i}", builder="b-1"))
        results = store.list_recent("b-1", "xp_gained", limit=5)
        assert len(results) == 5

    def test_list_recent_returns_all_when_less_than_limit(self):
        store = self.make_store()
        store.save(self.make_signal(builder="b-1"))
        results = store.list_recent("b-1", "xp_gained", limit=10)
        assert len(results) == 1

    def test_empty_store_returns_empty_lists(self):
        store = self.make_store()
        assert store.list_by_builder("b-1") == []
        assert store.list_recent("b-1", "xp_gained") == []
        assert store.get_by_observation("obs-1") == []
        assert store.count_all() == 0

    def test_list_by_builder_pagination(self):
        store = self.make_store()
        for i in range(10):
            store.save(self.make_signal(obs_id=f"obs-{i}", builder="b-1"))
        page1 = store.list_by_builder("b-1", limit=3, offset=0)
        page2 = store.list_by_builder("b-1", limit=3, offset=3)
        assert len(page1) == 3
        assert len(page2) == 3


# --- Direct Extraction Rules -------------------------------------------------


class TestXpGainedRule:
    def test_extracts_xp_from_mission_completed(self):
        from ascend.cognitive.extractor import XpGainedRule
        _reset_counter()
        obs = _make_obs("mission.completed", {"xpEarned": 150})
        result = XpGainedRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "xp_gained"
        assert result.value == 150
        assert result.confidence == 1.0

    def test_returns_none_when_missing_xp(self):
        from ascend.cognitive.extractor import XpGainedRule
        _reset_counter()
        obs = _make_obs("mission.completed", {})
        result = XpGainedRule().extract(obs, _ulid_counter)
        assert result is None

    def test_returns_none_for_wrong_type(self):
        from ascend.cognitive.extractor import XpGainedRule
        _reset_counter()
        obs = _make_obs("evidence.submitted", {"xpEarned": 150})
        result = XpGainedRule().extract(obs, _ulid_counter)
        assert result is None


class TestCompletionRateRule:
    def test_computes_rate_from_score(self):
        from ascend.cognitive.extractor import CompletionRateRule
        _reset_counter()
        obs = _make_obs("mission.completed", {"score": 85})
        result = CompletionRateRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "completion_rate"
        assert result.value == 0.85
        assert result.confidence == 1.0

    def test_defaults_to_zero_when_missing_score(self):
        from ascend.cognitive.extractor import CompletionRateRule
        _reset_counter()
        obs = _make_obs("mission.completed", {})
        result = CompletionRateRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.value == 0.0

    def test_clamps_rate_to_1_0(self):
        from ascend.cognitive.extractor import CompletionRateRule
        _reset_counter()
        obs = _make_obs("mission.completed", {"score": 200})
        result = CompletionRateRule().extract(obs, _ulid_counter)
        assert result.value == 1.0


class TestTimeSpentRule:
    def test_extracts_duration(self):
        from ascend.cognitive.extractor import TimeSpentRule
        _reset_counter()
        obs = _make_obs("mission.completed", {"duration": 1800})
        result = TimeSpentRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "time_spent"
        assert result.value == 1800

    def test_defaults_to_zero_when_missing(self):
        from ascend.cognitive.extractor import TimeSpentRule
        _reset_counter()
        obs = _make_obs("mission.completed", {})
        result = TimeSpentRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.value == 0


class TestScoreAchievedRule:
    def test_extracts_from_mission_completed(self):
        from ascend.cognitive.extractor import ScoreAchievedRule
        _reset_counter()
        obs = _make_obs("mission.completed", {"score": 85.5})
        result = ScoreAchievedRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "score_achieved"
        assert result.value == 85.5

    def test_extracts_from_assessment_completed(self):
        from ascend.cognitive.extractor import ScoreAchievedRule
        _reset_counter()
        obs = _make_obs("assessment.completed", {"score": 0.92})
        result = ScoreAchievedRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.value == 0.92

    def test_returns_none_when_missing_score(self):
        from ascend.cognitive.extractor import ScoreAchievedRule
        _reset_counter()
        obs = _make_obs("mission.completed", {})
        result = ScoreAchievedRule().extract(obs, _ulid_counter)
        assert result is None


class TestEvidenceQualityRule:
    def test_quality_from_content_length(self):
        from ascend.cognitive.extractor import EvidenceQualityRule
        _reset_counter()
        obs = _make_obs("evidence.submitted", {"content": "x" * 500})
        result = EvidenceQualityRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "evidence_quality"
        assert result.value == 0.5
        assert result.confidence == 0.7

    def test_quality_caps_at_1_0(self):
        from ascend.cognitive.extractor import EvidenceQualityRule
        _reset_counter()
        obs = _make_obs("evidence.submitted", {"content": "x" * 2000})
        result = EvidenceQualityRule().extract(obs, _ulid_counter)
        assert result.value == 1.0

    def test_no_content_returns_zero(self):
        from ascend.cognitive.extractor import EvidenceQualityRule
        _reset_counter()
        obs = _make_obs("evidence.submitted", {"content": ""})
        result = EvidenceQualityRule().extract(obs, _ulid_counter)
        assert result.value == 0.0


class TestTopicsCoveredRule:
    def test_counts_competencies(self):
        from ascend.cognitive.extractor import TopicsCoveredRule
        _reset_counter()
        obs = _make_obs("evidence.submitted", {"competencies": ["c1", "c2", "c3"]})
        result = TopicsCoveredRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "topics_covered"
        assert result.value == 3

    def test_empty_competencies_returns_zero(self):
        from ascend.cognitive.extractor import TopicsCoveredRule
        _reset_counter()
        obs = _make_obs("evidence.submitted", {"competencies": []})
        result = TopicsCoveredRule().extract(obs, _ulid_counter)
        assert result.value == 0


class TestCompetencyDepthRule:
    def test_extracts_level(self):
        from ascend.cognitive.extractor import CompetencyDepthRule
        _reset_counter()
        obs = _make_obs("competency.unlocked", {"level": 3})
        result = CompetencyDepthRule().extract(obs, _ulid_counter)
        assert result is not None
        assert result.type == "competency_depth"
        assert result.value == 3

    def test_defaults_to_level_1(self):
        from ascend.cognitive.extractor import CompetencyDepthRule
        _reset_counter()
        obs = _make_obs("competency.unlocked", {})
        result = CompetencyDepthRule().extract(obs, _ulid_counter)
        assert result.value == 1


# --- DirectExtractor ---------------------------------------------------------


class TestDirectExtractor:
    def test_dispatches_mission_completed(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("mission.completed", {
            "xpEarned": 150, "score": 85, "duration": 1800,
        })
        signals = extractor.extract(obs, _ulid_counter)
        types = {s.type for s in signals}
        assert "xp_gained" in types
        assert "completion_rate" in types
        assert "time_spent" in types
        assert "score_achieved" in types
        assert len(signals) == 4

    def test_dispatches_evidence_submitted(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("evidence.submitted", {
            "content": "x" * 300, "competencies": ["c1", "c2"],
        })
        signals = extractor.extract(obs, _ulid_counter)
        types = {s.type for s in signals}
        assert "evidence_quality" in types
        assert "topics_covered" in types
        assert len(signals) == 2

    def test_dispatches_competency_unlocked(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("competency.unlocked", {"level": 5})
        signals = extractor.extract(obs, _ulid_counter)
        assert len(signals) == 1
        assert signals[0].type == "competency_depth"

    def test_dispatches_assessment_completed(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("assessment.completed", {"score": 0.95})
        signals = extractor.extract(obs, _ulid_counter)
        assert len(signals) == 1
        assert signals[0].type == "score_achieved"

    def test_builder_created_returns_no_signals(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("builder.created", {"username": "alice"})
        signals = extractor.extract(obs, _ulid_counter)
        assert signals == []

    def test_achievement_earned_returns_no_signals(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("achievement.earned", {"name": "first_mission"})
        signals = extractor.extract(obs, _ulid_counter)
        assert signals == []

    def test_unmapped_type_returns_empty(self):
        _reset_counter()
        extractor = DirectExtractor()
        obs = _make_obs("unknown.event", {})
        signals = extractor.extract(obs, _ulid_counter)
        assert signals == []


# --- CompositeExtractor ------------------------------------------------------


class TestCompositeExtractor:
    def test_rolling_completion_rate(self):
        _reset_counter()
        store = InMemorySignalStore()
        for i in range(5):
            store.save(Signal(
                id=f"hist-{i}", observationId=f"obs-hist-{i}",
                type="completion_rate", value=0.8 + i * 0.04,
                confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                metadata={"builderId": "builder-1"},
            ))
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"score": 90})
        direct = [Signal(
            id="direct-1", observationId="obs-1",
            type="completion_rate", value=0.9,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        )]
        signals = composite.extract(obs, direct, _ulid_counter)
        rolling = [s for s in signals if s.type == "rolling_completion_rate"]
        assert len(rolling) == 1
        assert rolling[0].confidence == 0.5
        assert rolling[0].value == 0.88

    def test_rolling_avg_xp(self):
        _reset_counter()
        store = InMemorySignalStore()
        for i in range(3):
            store.save(Signal(
                id=f"hist-{i}", observationId=f"obs-hist-{i}",
                type="xp_gained", value=100 + i * 50,
                confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                metadata={"builderId": "builder-1"},
            ))
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"xpEarned": 200})
        direct = [Signal(
            id="direct-1", observationId="obs-1",
            type="xp_gained", value=200,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        )]
        signals = composite.extract(obs, direct, _ulid_counter)
        rolling = [s for s in signals if s.type == "rolling_avg_xp"]
        assert len(rolling) == 1
        assert rolling[0].confidence == 0.3

    def test_rolling_avg_score(self):
        _reset_counter()
        store = InMemorySignalStore()
        for i in range(4):
            store.save(Signal(
                id=f"hist-{i}", observationId=f"obs-hist-{i}",
                type="score_achieved", value=70 + i * 5,
                confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                metadata={"builderId": "builder-1"},
            ))
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"score": 90})
        direct = [Signal(
            id="direct-1", observationId="obs-1",
            type="score_achieved", value=90.0,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        )]
        signals = composite.extract(obs, direct, _ulid_counter)
        rolling = [s for s in signals if s.type == "rolling_avg_score"]
        assert len(rolling) == 1

    def test_xp_per_minute(self):
        _reset_counter()
        store = InMemorySignalStore()
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"xpEarned": 150, "duration": 600})
        direct = [
            Signal(id="d1", observationId="obs-1", type="xp_gained", value=150,
                   confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                   metadata={"builderId": "builder-1"}),
            Signal(id="d2", observationId="obs-1", type="time_spent", value=600,
                   confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                   metadata={"builderId": "builder-1"}),
        ]
        signals = composite.extract(obs, direct, _ulid_counter)
        xpm = [s for s in signals if s.type == "xp_per_minute"]
        assert len(xpm) == 1
        assert xpm[0].value == pytest.approx(15.0)

    def test_xp_per_minute_skipped_when_no_time(self):
        _reset_counter()
        store = InMemorySignalStore()
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"xpEarned": 150, "duration": 0})
        direct = [
            Signal(id="d1", observationId="obs-1", type="xp_gained", value=150,
                   confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                   metadata={"builderId": "builder-1"}),
            Signal(id="d2", observationId="obs-1", type="time_spent", value=0,
                   confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                   metadata={"builderId": "builder-1"}),
        ]
        signals = composite.extract(obs, direct, _ulid_counter)
        xpm = [s for s in signals if s.type == "xp_per_minute"]
        assert len(xpm) == 0

    def test_streak_active_when_no_history(self):
        _reset_counter()
        store = InMemorySignalStore()
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"score": 90})
        direct = [Signal(
            id="d1", observationId="obs-1", type="completion_rate", value=0.9,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        )]
        signals = composite.extract(obs, direct, _ulid_counter)
        sa = [s for s in signals if s.type == "streak_active"]
        assert len(sa) == 1
        assert sa[0].value is False
        assert sa[0].confidence == 0.8

    def test_streak_active_with_history(self):
        _reset_counter()
        store = InMemorySignalStore()
        store.save(Signal(
            id="hist-1", observationId="obs-hist-1",
            type="time_spent", value=300,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        ))
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"score": 90})
        direct = [Signal(
            id="d1", observationId="obs-1", type="completion_rate", value=0.9,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        )]
        signals = composite.extract(obs, direct, _ulid_counter)
        sa = [s for s in signals if s.type == "streak_active"]
        assert len(sa) == 1
        assert sa[0].value is True
        assert sa[0].confidence == 1.0

    def test_streak_length(self):
        _reset_counter()
        store = InMemorySignalStore()
        for i in range(3):
            store.save(Signal(
                id=f"hist-{i}", observationId=f"obs-hist-{i}",
                type="time_spent", value=300,
                confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
                metadata={"builderId": "builder-1"},
            ))
        composite = CompositeExtractor(store)
        obs = _make_obs("mission.completed", {"score": 90})
        direct = [Signal(
            id="d1", observationId="obs-1", type="completion_rate", value=0.9,
            confidence=1.0, extractedAt="2026-07-21T12:00:00Z",
            metadata={"builderId": "builder-1"},
        )]
        signals = composite.extract(obs, direct, _ulid_counter)
        sl = [s for s in signals if s.type == "streak_length"]
        assert len(sl) == 1
        assert sl[0].value == 3
        assert sl[0].confidence == 3.0 / 7.0

    def test_no_composites_when_no_matching_direct_types(self):
        _reset_counter()
        store = InMemorySignalStore()
        composite = CompositeExtractor(store)
        obs = _make_obs("builder.created", {})
        signals = composite.extract(obs, [], _ulid_counter)
        assert signals == []


# --- SignalExtractor (Integration) -------------------------------------------


class TestSignalExtractor:
    def test_extract_mission_returns_direct_and_composite(self):
        _reset_counter()
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        obs = _make_obs("mission.completed", {
            "xpEarned": 150, "score": 85, "duration": 1800,
        })
        signals = extractor.extract(obs)
        assert len(signals) >= 4
        types = {s.type for s in signals}
        assert "xp_gained" in types
        assert "completion_rate" in types
        assert "time_spent" in types
        assert "score_achieved" in types

    def test_signals_persisted_in_store(self):
        _reset_counter()
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        obs = _make_obs("mission.completed", {
            "xpEarned": 150, "score": 85, "duration": 1800,
        })
        extractor.extract(obs)
        assert store.count_all() >= 4

    def test_evidence_submitted_produces_two_signals(self):
        _reset_counter()
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        obs = _make_obs("evidence.submitted", {
            "content": "detailed analysis here", "competencies": ["c1"],
        })
        signals = extractor.extract(obs)
        types = {s.type for s in signals}
        assert "evidence_quality" in types
        assert "topics_covered" in types

    def test_competency_unlocked_produces_depth_signal(self):
        _reset_counter()
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        obs = _make_obs("competency.unlocked", {"level": 7})
        signals = extractor.extract(obs)
        assert len(signals) == 1
        assert signals[0].type == "competency_depth"
        assert signals[0].value == 7

    def test_builder_created_produces_no_signals(self):
        _reset_counter()
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        obs = _make_obs("builder.created", {"username": "alice"})
        signals = extractor.extract(obs)
        assert signals == []

    def test_achievement_earned_produces_no_signals(self):
        _reset_counter()
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        obs = _make_obs("achievement.earned", {"name": "first_mission"})
        signals = extractor.extract(obs)
        assert signals == []

    def test_deterministic_with_same_observation(self):
        store1 = InMemorySignalStore()
        store2 = InMemorySignalStore()
        _reset_counter()
        extractor1 = SignalExtractor(store1, ulid_factory=_ulid_counter)
        obs = _make_obs("mission.completed", {
            "xpEarned": 150, "score": 85, "duration": 1800,
        })
        sigs1 = extractor1.extract(obs)

        _reset_counter()
        extractor2 = SignalExtractor(store2, ulid_factory=_ulid_counter)
        sigs2 = extractor2.extract(obs)

        assert len(sigs1) == len(sigs2)
        for s1, s2 in zip(sigs1, sigs2):
            assert s1.type == s2.type
            assert s1.value == s2.value
            assert s1.confidence == s2.confidence

    def test_store_property(self):
        store = InMemorySignalStore()
        extractor = SignalExtractor(store, ulid_factory=_ulid_counter)
        assert extractor.store is store


# --- Confidence Decay --------------------------------------------------------


class TestConfidenceDecay:
    def test_no_decay_for_fresh_signal(self):
        assert confidence_decay(1.0, 0) == 1.0

    def test_partial_decay(self):
        c = confidence_decay(1.0, 90)
        assert c == pytest.approx(0.5)

    def test_minimum_floor(self):
        c = confidence_decay(1.0, 180)
        assert c == 0.5

    def test_beyond_floor(self):
        c = confidence_decay(1.0, 365)
        assert c == 0.5

    def test_proportional_decay(self):
        c = confidence_decay(0.8, 45)
        assert c == pytest.approx(0.8 * (1.0 - 45 / 180))

    def test_decay_example(self):
        c = confidence_decay(0.7, 90)
        assert c == 0.35
