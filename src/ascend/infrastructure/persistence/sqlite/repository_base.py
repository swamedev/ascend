import sqlite3
from typing import Any

from .connection import ConnectionManager


class SQLiteRepositoryBase:
    def __init__(self, conn_manager: ConnectionManager) -> None:
        self._conn_manager = conn_manager

    @property
    def _conn(self) -> sqlite3.Connection:
        return self._conn_manager.get_connection()

    def _execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def _executemany(self, sql: str, params: list[tuple]) -> sqlite3.Cursor:
        return self._conn.executemany(sql, params)

    def _fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        row = self._conn.execute(sql, params).fetchone()
        return dict(row) if row else None

    def _fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
