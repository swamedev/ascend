from ascend.cognitive.models import (
    InMemoryObservationStore,
    InMemorySignalStore,
    InMemoryPatternStore,
    InMemoryInsightStore,
    InMemoryRecommendationStore,
    Observation,
    Signal,
    Pattern,
    Insight,
    Recommendation,
    SignalType,
    PatternType,
    InsightType,
    InsightSeverity,
    RecommendationType,
    RecommendationPriority,
)
from ascend.cognitive.timeline import (
    TimelineBuilder,
    ReplayEngine,
    SnapshotBuilder,
    EvolutionView,
)

_BUILDER_ID = "builder-test-001"
_ulid_counter: int = 0


def _ulid() -> str:
    global _ulid_counter
    _ulid_counter += 1
    return "ulid-" + str(_ulid_counter).zfill(6)


def _now() -> str:
    return "2026-07-21T12:00:00Z"


def _seed_stores() -> tuple:
    obs_store = InMemoryObservationStore()
    sig_store = InMemorySignalStore()
    pat_store = InMemoryPatternStore()
    ins_store = InMemoryInsightStore()
    rec_store = InMemoryRecommendationStore()

    obs = Observation(
        id=_ulid(), type="mission.completed", source="runtime",
        timestamp=_now(), data={}, context={"builderId": _BUILDER_ID},
    )
    obs_store.save(obs)

    sig = Signal(
        id=_ulid(), observationId=obs.id, type=SignalType.COMPLETION_RATE.value,
        value=0.85, confidence=1.0, extractedAt=_now(),
        metadata={"builderId": _BUILDER_ID},
    )
    sig_store.save(sig)

    pat = Pattern(
        id=_ulid(), pattern_type=PatternType.TREND_UP.value,
        label="Trend up", value=0.2, confidence=1.0,
        source_signal_ids=[sig.id], observed_at=_now(),
        metadata={"builderId": _BUILDER_ID},
    )
    pat_store.save(pat)

    ins = Insight(
        id=_ulid(), insight_type=InsightType.ACCELERATING_GROWTH.value,
        title="Growing", description="XP growing", severity=InsightSeverity.INFO.value,
        confidence=1.0, source_pattern_ids=[pat.id], generated_at=_now(),
        metadata={"builderId": _BUILDER_ID},
    )
    ins_store.save(ins)

    rec = Recommendation(
        id=_ulid(), recommendation_type=RecommendationType.ADVANCE_CONTENT.value,
        title="Advance", description="Try harder content",
        priority=RecommendationPriority.MEDIUM.value,
        source_insight_ids=[ins.id], generated_at=_now(),
        metadata={"builderId": _BUILDER_ID},
    )
    rec_store.save(rec)

    return obs_store, sig_store, pat_store, ins_store, rec_store


# ─── TimelineBuilder ────────────────────────────────────────────────────────


class TestTimelineBuilder:
    def test_build_full_timeline(self) -> None:
        stores = _seed_stores()
        builder = TimelineBuilder(*stores)
        result = builder.build(_BUILDER_ID)
        assert result["builder_id"] == _BUILDER_ID
        assert len(result["observations"]) == 1
        assert len(result["signals"]) == 1
        assert len(result["patterns"]) == 1
        assert len(result["insights"]) == 1
        assert len(result["recommendations"]) == 1

    def test_empty_builder_returns_empty(self) -> None:
        builder = TimelineBuilder(
            InMemoryObservationStore(),
            InMemorySignalStore(),
            InMemoryPatternStore(),
            InMemoryInsightStore(),
            InMemoryRecommendationStore(),
        )
        result = builder.build(_BUILDER_ID)
        assert len(result["observations"]) == 0
        assert len(result["signals"]) == 0
        assert len(result["patterns"]) == 0
        assert len(result["insights"]) == 0
        assert len(result["recommendations"]) == 0

    def test_different_builder_isolation(self) -> None:
        stores = _seed_stores()
        builder = TimelineBuilder(*stores)
        result = builder.build("other-builder")
        assert len(result["observations"]) == 0

    def test_determinism(self) -> None:
        stores1 = _seed_stores()
        builder1 = TimelineBuilder(*stores1)
        r1 = builder1.build(_BUILDER_ID)

        stores2 = _seed_stores()
        global _ulid_counter
        _ulid_counter = 0
        builder2 = TimelineBuilder(*stores2)
        r2 = builder2.build(_BUILDER_ID)

        assert len(r1["observations"]) == len(r2["observations"])
        assert len(r1["signals"]) == len(r2["signals"])


# ─── ReplayEngine ───────────────────────────────────────────────────────────


class TestReplayEngine:
    def test_replay_returns_timeline(self) -> None:
        stores = _seed_stores()
        builder = TimelineBuilder(*stores)
        engine = ReplayEngine(builder)
        result = engine.replay(_BUILDER_ID, "2026-01-01T00:00:00Z", "2026-12-31T23:59:59Z")
        assert len(result["observations"]) == 1

    def test_replay_out_of_range(self) -> None:
        stores = _seed_stores()
        builder = TimelineBuilder(*stores)
        engine = ReplayEngine(builder)
        result = engine.replay(_BUILDER_ID, "2025-01-01T00:00:00Z", "2025-12-31T23:59:59Z")
        assert len(result["observations"]) == 0


# ─── SnapshotBuilder ────────────────────────────────────────────────────────


class TestSnapshotBuilder:
    def test_snapshot_returns_current_state(self) -> None:
        stores = _seed_stores()
        _, sig, pat, ins, rec = stores
        builder = SnapshotBuilder(sig, pat, ins, rec)
        snap = builder.snapshot(_BUILDER_ID)
        assert snap.builder_id == _BUILDER_ID
        assert len(snap.signals) == 1
        assert len(snap.patterns) == 1
        assert len(snap.insights) == 1
        assert len(snap.recommendations) == 1
        assert "signal_count" in snap.summary

    def test_empty_snapshot(self) -> None:
        builder = SnapshotBuilder(
            InMemorySignalStore(),
            InMemoryPatternStore(),
            InMemoryInsightStore(),
            InMemoryRecommendationStore(),
        )
        snap = builder.snapshot(_BUILDER_ID)
        assert snap.builder_id == _BUILDER_ID
        assert len(snap.signals) == 0


# ─── EvolutionView ──────────────────────────────────────────────────────────


class TestEvolutionView:
    def test_compare_returns_metrics(self) -> None:
        stores = _seed_stores()
        _, sig, pat, _, _ = stores
        view = EvolutionView(sig, pat)
        from ascend.cognitive.models import EvolutionPeriod
        period = EvolutionPeriod(start="2026-01-01T00:00:00Z", end="2026-12-31T23:59:59Z")
        result = view.compare(_BUILDER_ID, period)
        assert result.builder_id == _BUILDER_ID
        assert result.xp_growth >= 0
        assert isinstance(result.strengths, list)
        assert isinstance(result.weaknesses, list)

    def test_90_day_evolution(self) -> None:
        stores = _seed_stores()
        _, sig, pat, _, _ = stores
        view = EvolutionView(sig, pat)
        result = view.evolution_over_90_days(_BUILDER_ID)
        assert result.builder_id == _BUILDER_ID
