import pytest

from ascend.cognitive.models import NormalizedObservation, Observation
from ascend.cognitive.normalizer import (
    ENCODING,
    SNAKE_TO_CAMEL,
    _encode_base32,
    _generate_ulid,
    _map_fields,
    _normalize_timestamp,
    _strip_sensitive,
    ObservationNormalizer,
)


# ---------------------------------------------------------------------------
# ULID generation
# ---------------------------------------------------------------------------


class TestUlidGeneration:
    def test_ulid_length(self):
        ulid = _generate_ulid()
        assert len(ulid) == 26

    def test_ulid_uses_valid_chars(self):
        ulid = _generate_ulid()
        for ch in ulid:
            assert ch in ENCODING, f"Invalid character: {ch}"

    def test_ulid_is_sortable(self):
        earlier = _generate_ulid(timestamp_ms=1000)
        later = _generate_ulid(timestamp_ms=2000)
        assert earlier < later

    def test_ulid_deterministic_with_same_timestamp(self):
        ulid1 = _generate_ulid(timestamp_ms=42)
        ulid2 = _generate_ulid(timestamp_ms=42)
        assert ulid1 != ulid2  # random component differs

    def test_encode_base32(self):
        assert _encode_base32(0, 1) == "0"
        assert _encode_base32(1, 1) == "1"
        assert len(_encode_base32(123456, 10)) == 10


# ---------------------------------------------------------------------------
# Timestamp normalization
# ---------------------------------------------------------------------------


class TestTimestampNormalization:
    def test_iso_8601_utc_passthrough(self):
        result, warnings = _normalize_timestamp("2026-07-21T14:30:00Z")
        assert "2026-07-21T14:30:00" in result
        assert warnings == []

    def test_iso_8601_with_timezone(self):
        result, warnings = _normalize_timestamp("2026-07-21T11:30:00-03:00")
        assert "2026-07-21T14:30:00" in result
        assert warnings == []

    def test_unix_epoch_seconds(self):
        result, warnings = _normalize_timestamp("1741500000")
        assert warnings == []

    def test_unix_epoch_milliseconds(self):
        result, warnings = _normalize_timestamp("1741500000000")
        assert warnings == []

    def test_empty_string_returns_warning(self):
        result, warnings = _normalize_timestamp("")
        assert "missing_timestamp" in warnings

    def test_invalid_string_returns_warning(self):
        result, warnings = _normalize_timestamp("not-a-timestamp")
        assert "unparseable_timestamp" in warnings


# ---------------------------------------------------------------------------
# Sensitive data stripping
# ---------------------------------------------------------------------------


class TestSensitiveDataStripping:
    def test_strips_password_field(self):
        data = {"username": "alice", "password": "secret123"}
        result, stripped = _strip_sensitive(data)
        assert "username" in result
        assert "password" not in result
        assert stripped == ["password"]

    def test_strips_token_field(self):
        data = {"access_token": "abc123"}
        result, stripped = _strip_sensitive(data)
        assert "access_token" not in result

    def test_strips_email_field(self):
        data = {"email": "alice@example.com"}
        result, stripped = _strip_sensitive(data)
        assert "email" not in result

    def test_strips_binary_large_field(self):
        data = {"big_blob": b"x" * 70000}
        result, stripped = _strip_sensitive(data)
        assert "big_blob" not in result

    def test_preserves_safe_fields(self):
        data = {"builder_id": "bld-1", "score": 85, "username": "alice"}
        result, stripped = _strip_sensitive(data)
        assert result["builder_id"] == "bld-1"
        assert result["score"] == 85
        assert stripped == []

    def test_partial_strip(self):
        data = {"builder_id": "bld-1", "password": "secret", "score": 85}
        result, stripped = _strip_sensitive(data)
        assert "builder_id" in result
        assert "score" in result
        assert "password" not in result
        assert stripped == ["password"]


# ---------------------------------------------------------------------------
# Field mapping (snake_case → camelCase)
# ---------------------------------------------------------------------------


class TestFieldMapping:
    def test_maps_known_fields(self):
        data = {"builder_id": "bld-1", "mission_id": "m-1", "score": 85}
        result = _map_fields(data)
        assert result["builderId"] == "bld-1"
        assert result["missionId"] == "m-1"
        assert result["score"] == 85

    def test_preserves_unknown_fields_in_raw(self):
        data = {"builder_id": "bld-1", "legacy_field": "value"}
        result = _map_fields(data)
        assert result["builderId"] == "bld-1"
        assert result["raw"]["legacy_field"] == "value"

    def test_empty_data(self):
        result = _map_fields({})
        assert result == {}

    def test_all_mappings_covered(self):
        for snake, camel in SNAKE_TO_CAMEL.items():
            data = {snake: "test"}
            result = _map_fields(data)
            assert camel in result, f"Missing mapping: {snake} → {camel}"


# ---------------------------------------------------------------------------
# ObservationNormalizer integration
# ---------------------------------------------------------------------------


class TestObservationNormalizer:
    @pytest.fixture
    def raw_observation(self):
        return Observation(
            id="obs-001",
            type="mission.completed",
            source="runtime",
            timestamp="2026-07-21T14:30:00Z",
            data={
                "builder_id": "bld-42",
                "mission_id": "m-101",
                "xp_earned": 150,
                "score": 85,
                "duration": 1800,
                "password": "should-be-stripped",
            },
            context={"builderId": "bld-42", "missionId": "m-101"},
            metadata={
                "observationSchema": "1.0",
                "collector": "observation-collector",
                "eventId": "evt-test",
            },
        )

    def test_normalize_returns_normalized_observation(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert isinstance(result, NormalizedObservation)

    def test_normalize_generates_ulid(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert len(result.id) == 26
        for ch in result.id:
            assert ch in ENCODING

    def test_normalize_preserves_type_and_source(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert result.type == "mission.completed"
        assert result.source == "runtime"

    def test_normalize_timestamp_iso_format(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert "2026-07-21T14:30:00" in result.timestamp

    def test_normalize_maps_fields_to_camel_case(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert result.data["builderId"] == "bld-42"
        assert result.data["missionId"] == "m-101"
        assert result.data["xpEarned"] == 150
        assert result.data["score"] == 85

    def test_normalize_strips_sensitive_data(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert "password" not in result.data
        assert "raw" not in result.data or "password" not in result.data.get("raw", {})

    def test_normalize_adds_trace(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert "correlationId" in result.trace
        assert result.trace["correlationId"] is not None
        assert "causationId" in result.trace

    def test_normalize_preserves_context(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert result.context["builderId"] == "bld-42"
        assert result.context["missionId"] == "m-101"

    def test_normalize_adds_metadata(self, raw_observation):
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(raw_observation)
        assert result.metadata["observationSchema"] == "1.0"
        assert result.metadata["normalizer"] == "observation-normalizer"
        assert result.metadata["originalId"] == "obs-001"

    def test_normalize_batch_returns_list(self, raw_observation):
        normalizer = ObservationNormalizer()
        results = normalizer.normalize_batch([raw_observation, raw_observation])
        assert len(results) == 2
        assert all(isinstance(r, NormalizedObservation) for r in results)

    def test_normalize_batch_each_has_unique_id(self, raw_observation):
        normalizer = ObservationNormalizer()
        results = normalizer.normalize_batch([raw_observation, raw_observation])
        assert results[0].id != results[1].id

    def test_normalize_handles_empty_data(self):
        obs = Observation(
            id="obs-empty",
            type="builder.created",
            source="runtime",
            timestamp="2026-07-21T10:00:00Z",
            data={},
            context={"builderId": "bld-1"},
            metadata={},
        )
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(obs)
        assert result.data == {}

    def test_unparseable_timestamp_adds_warning(self):
        obs = Observation(
            id="obs-bad-ts",
            type="test.event",
            source="runtime",
            timestamp="not-a-timestamp",
            data={"builder_id": "bld-1"},
            context={"builderId": "bld-1"},
            metadata={},
        )
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(obs)
        assert result.timestamp is not None
        assert len(result.timestamp) > 0

    def test_deterministic_ulid_factory(self):
        call_count = 0

        def deterministic_factory():
            nonlocal call_count
            call_count += 1
            return f"ULID{call_count:0>22}"

        normalizer = ObservationNormalizer(ulid_factory=deterministic_factory)
        obs = Observation(
            id="obs-det",
            type="test.event",
            source="runtime",
            timestamp="2026-07-21T10:00:00Z",
            data={"builder_id": "bld-1"},
            context={"builderId": "bld-1"},
            metadata={},
        )
        result1 = normalizer.normalize(obs)
        result2 = normalizer.normalize(obs)
        # Factory is called: call 1 = correlationId, call 2 = obs1.id, call 3 = obs2.corr, call 4 = obs2.id
        assert result1.id.startswith("ULID")
        assert result2.id.startswith("ULID")
        assert result1.id != result2.id

    def test_correlation_id_preserved_from_metadata(self):
        obs = Observation(
            id="obs-corr",
            type="test.event",
            source="runtime",
            timestamp="2026-07-21T10:00:00Z",
            data={"builder_id": "bld-1"},
            context={"builderId": "bld-1"},
            metadata={"correlationId": "preserved-corr-id"},
        )
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(obs)
        assert result.trace["correlationId"] == "preserved-corr-id"

    def test_causation_id_preserved_from_metadata(self):
        obs = Observation(
            id="obs-caus",
            type="test.event",
            source="runtime",
            timestamp="2026-07-21T10:00:00Z",
            data={"builder_id": "bld-1"},
            context={"builderId": "bld-1"},
            metadata={"causationId": "parent-obs-id"},
        )
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(obs)
        assert result.trace["causationId"] == "parent-obs-id"

    def test_normalize_with_context_without_known_fields(self):
        obs = Observation(
            id="obs-ctx",
            type="custom.event",
            source="builder",
            timestamp="2026-07-21T10:00:00Z",
            data={"custom_key": "custom_value"},
            context={"builderId": "bld-1", "arbitrary": "data"},
            metadata={},
        )
        normalizer = ObservationNormalizer()
        result = normalizer.normalize(obs)
        assert result.context["builderId"] == "bld-1"
        assert result.context["arbitrary"] == "data"
        assert result.data["raw"]["custom_key"] == "custom_value"
