from .persistence.sqlite.connection import ConnectionManager


class UnitOfWork:
    def __init__(self, conn_manager: ConnectionManager) -> None:
        self._conn_manager = conn_manager

    def __enter__(self) -> "UnitOfWork":
        conn = self._conn_manager.get_connection()
        conn.execute("BEGIN")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        conn = self._conn_manager.get_connection()
        if exc_type is not None:
            conn.rollback()
        else:
            conn.commit()

    def commit(self) -> None:
        conn = self._conn_manager.get_connection()
        conn.commit()

    def rollback(self) -> None:
        conn = self._conn_manager.get_connection()
        conn.rollback()
