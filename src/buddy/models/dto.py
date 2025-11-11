from dataclasses import dataclass

from src.buddy import models


@dataclass
class Result:
    normalized: models.objects.Position
    horizontal: models.states.Horizontal
    vertical: models.states.Vertical
    distance: models.states.Distance
