from dataclasses import dataclass


@dataclass(frozen=True)
class XP:
    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"XP cannot be negative: {self.amount}")

    def __add__(self, other: "XP") -> "XP":
        return XP(self.amount + other.amount)


@dataclass(frozen=True)
class Level:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError(f"Level must be >= 1: {self.value}")

    def __add__(self, other: int) -> "Level":
        return Level(self.value + other)
