from dataclasses import dataclass


@dataclass
class Window:
    name: str
    width: int
    height: int
    fullscreen: bool


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Face:
    position: Position
    width: int
    height: int


@dataclass
class Result:
    normalized: Position
    horizontal: str
    vertical: str
    distance: str
