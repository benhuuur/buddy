from dataclasses import dataclass


@dataclass(frozen=True)
class Thresholds:
    LEFT: float = 0.35
    RIGHT: float = 0.65
    TOP: float = 0.35
    BOTTOM: float = 0.65

    CLOSE: float = 0.18
    MEDIUM: float = 0.08
