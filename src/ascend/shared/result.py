from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Result(Generic[T, E]):
    _value: Optional[T] = None
    _error: Optional[E] = None

    @property
    def is_ok(self) -> bool:
        return self._error is None

    @property
    def is_err(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self._error is not None:
            raise RuntimeError(f"Called unwrap on error: {self._error}")
        return self._value

    def unwrap_err(self) -> E:
        if self._value is not None:
            raise RuntimeError("Called unwrap_err on ok value")
        return self._error


def Ok(value: T) -> Result[T, E]:
    return Result(_value=value)


def Err(error: E) -> Result[T, E]:
    return Result(_error=error)
