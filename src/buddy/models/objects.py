from typing import Union
from dataclasses import dataclass


@dataclass
class Position:
    x: Union[int, float]
    y: Union[int, float]


@dataclass
class Size:
    width: Union[int, float]
    height: Union[int, float]


@dataclass
class Rectangle:
    position: Position
    size: Size
