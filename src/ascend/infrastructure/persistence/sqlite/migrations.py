from .connection import ConnectionManager

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS builders (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    level INTEGER NOT NULL DEFAULT 1,
    xp INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS competencies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    level INTEGER NOT NULL DEFAULT 1,
    criteria TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS builder_competencies (
    builder_id TEXT NOT NULL REFERENCES builders(id),
    competency_id TEXT NOT NULL REFERENCES competencies(id),
    level INTEGER NOT NULL DEFAULT 1,
    progress REAL NOT NULL DEFAULT 0.0,
    evidence_count INTEGER NOT NULL DEFAULT 0,
    last_update TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (builder_id, competency_id)
);

CREATE TABLE IF NOT EXISTS missions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    objective TEXT NOT NULL DEFAULT '',
    difficulty INTEGER NOT NULL DEFAULT 1,
    xp_reward INTEGER NOT NULL DEFAULT 100,
    status TEXT NOT NULL DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS builder_missions (
    builder_id TEXT NOT NULL REFERENCES builders(id),
    mission_id TEXT NOT NULL REFERENCES missions(id),
    status TEXT NOT NULL DEFAULT 'available',
    PRIMARY KEY (builder_id, mission_id)
);

CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL REFERENCES builders(id),
    mission_id TEXT NOT NULL REFERENCES missions(id),
    artifact TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'document',
    status TEXT NOT NULL DEFAULT 'submitted',
    submitted_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS assessments (
    id TEXT PRIMARY KEY,
    evidence_id TEXT NOT NULL REFERENCES evidence(id),
    reviewer TEXT NOT NULL DEFAULT '',
    score REAL NOT NULL DEFAULT 0.0,
    feedback TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    criteria TEXT NOT NULL DEFAULT '[]',
    badge TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS builder_achievements (
    builder_id TEXT NOT NULL REFERENCES builders(id),
    achievement_id TEXT NOT NULL REFERENCES achievements(id),
    earned_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (builder_id, achievement_id)
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS journeys (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now')),
    description TEXT NOT NULL DEFAULT ''
);
"""


class MigrationEngine:
    def __init__(self, conn_manager: ConnectionManager) -> None:
        self._conn_manager = conn_manager

    def apply_all(self) -> None:
        conn = self._conn_manager.get_connection()
        conn.executescript(SCHEMA_SQL)
