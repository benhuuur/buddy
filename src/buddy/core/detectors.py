import cv2
import numpy

from abc import ABC, abstractmethod

from src.buddy import models



class Detector(ABC):
    @abstractmethod
    def detect(self, frame: numpy.ndarray) -> list[models.objects.Rectangle]:
        raise NotImplementedError(
            "Subclasses must implement the detect() method.")


class Cascade(Detector):
    def __init__(self, ratio: float = 1):
        self.ratio = ratio

        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.classifier = cv2.CascadeClassifier(path)

    def detect(self, frame: numpy.ndarray) -> list[models.objects.Rectangle]:
        faces = []
        height, width, channels = frame.shape

        resized = cv2.resize(
            frame, (int(width * self.ratio), int(height * self.ratio)))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in self.classifier.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        ):
            face = models.objects.Rectangle(
                models.objects.Position(x / self.ratio, y / self.ratio),
                models.objects.Size(int(w / self.ratio), int(h / self.ratio))
            )
            faces.append(face)
        return faces
