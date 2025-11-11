from enum import Enum

from src.buddy.models.configs import Thresholds



class Horizontal(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"

    @staticmethod
    def classify(normalized: float):
        if normalized < Thresholds.LEFT:
            return Horizontal.LEFT
        elif normalized > Thresholds.RIGHT:
            return Horizontal.RIGHT
        return Horizontal.CENTER


class Vertical(Enum):
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    CENTER = "CENTER"

    @staticmethod
    def classify(normalized: float):
        if normalized < Thresholds.TOP:
            return Vertical.TOP
        elif normalized > Thresholds.BOTTOM:
            return Vertical.BOTTOM
        return Vertical.CENTER


class Distance(Enum):
    CLOSE = "CLOSE"
    MEDIUM = "MEDIUM"
    FAR = "FAR"

    @staticmethod
    def classify(ratio: float):
        if ratio > Thresholds.CLOSE:
            return Distance.CLOSE
        elif ratio > Thresholds.MEDIUM:
            return Distance.MEDIUM
        return Distance.FAR
