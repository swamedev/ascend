import re
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

from .models import (
    SENSITIVE_PATTERNS,
    NormalizedObservation,
    Observation,
)

SNAKE_TO_CAMEL: dict[str, str] = {
    "builder_id": "builderId",
    "mission_id": "missionId",
    "evidence_id": "evidenceId",
    "assessment_id": "assessmentId",
    "competency_id": "competencyId",
    "achievement_id": "achievementId",
    "journey_id": "journeyId",
    "session_id": "sessionId",
    "xp_earned": "xpEarned",
    "xp_reward": "xpReward",
    "artifact": "content",
    "username": "username",
    "display_name": "displayName",
    "level": "level",
    "score": "score",
}

ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _generate_ulid(timestamp_ms: int | None = None) -> str:
    import secrets
    if timestamp_ms is None:
        timestamp_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    ts_part = _encode_base32(timestamp_ms, 10)
    random_part = _encode_base32(
        secrets.randbits(80), 16
    )
    return ts_part + random_part


def _encode_base32(value: int, length: int) -> str:
    result: list[str] = []
    for _ in range(length):
        result.append(ENCODING[value & 0x1F])
        value >>= 5
    return "".join(reversed(result))


def _strip_sensitive(data: dict[str, Any]) -> dict[str, Any]:
    stripped: list[str] = []
    result: dict[str, Any] = {}
    for key, value in data.items():
        key_lower = key.lower()
        if any(pattern in key_lower for pattern in SENSITIVE_PATTERNS):
            stripped.append(key)
            continue
        if isinstance(value, (bytes, bytearray)) and len(value) > 65536:
            stripped.append(key)
            continue
        if isinstance(value, str) and len(value.encode("utf-8")) > 65536:
            stripped.append(key)
            continue
        result[key] = value
    return result, stripped


def _normalize_timestamp(raw_ts: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    parsed: datetime | None = None

    if not raw_ts:
        warnings.append("missing_timestamp")
        return datetime.now(timezone.utc).isoformat(), warnings

    try:
        parsed = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        pass

    if parsed is None:
        try:
            ts_float = float(raw_ts)
            if ts_float > 1e12:
                ts_float /= 1000
            parsed = datetime.fromtimestamp(ts_float, tz=timezone.utc)
        except (ValueError, OverflowError, TypeError):
            pass

    if parsed is None:
        warnings.append("unparseable_timestamp")
        return datetime.now(timezone.utc).isoformat(), warnings

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)

    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ"), warnings


def _map_fields(data: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    raw: dict[str, Any] = {}
    for key, value in data.items():
        camel = SNAKE_TO_CAMEL.get(key)
        if camel is not None:
            result[camel] = value
        else:
            raw[key] = value
    if raw:
        result["raw"] = raw
    return result


class ObservationNormalizer:
    def __init__(
        self,
        ulid_factory: Callable[[], str] | None = None,
    ) -> None:
        self._ulid_factory = ulid_factory or _generate_ulid
        self._correlation_factory: Callable[[], str] = self._ulid_factory

    def normalize(self, observation: Observation) -> NormalizedObservation:
        ts, ts_warnings = _normalize_timestamp(observation.timestamp)

        stripped_data, stripped_fields = _strip_sensitive(observation.data)
        mapped_data = _map_fields(stripped_data)

        warnings: list[str] = list(ts_warnings)
        if stripped_fields:
            warnings.append(f"stripped_fields:{','.join(stripped_fields)}")

        correlation_id = observation.metadata.get("correlationId") or self._correlation_factory()

        return NormalizedObservation(
            id=self._ulid_factory(),
            type=observation.type,
            source=observation.source,
            timestamp=ts,
            data=mapped_data,
            context=dict(observation.context),
            metadata={
                "observationSchema": "1.0",
                "normalizer": "observation-normalizer",
                "normalizedAt": datetime.now(timezone.utc).isoformat(),
                "originalId": observation.id,
                "originalMetadata": dict(observation.metadata),
            },
            trace={
                "correlationId": correlation_id,
                "causationId": observation.metadata.get("causationId"),
            },
        )

    def normalize_batch(
        self,
        observations: list[Observation],
    ) -> list[NormalizedObservation]:
        return [self.normalize(o) for o in observations]
