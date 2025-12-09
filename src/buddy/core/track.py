import cv2
import numpy
import queue
import threading

from src.buddy import models, utils
from src.buddy.core.detectors import Detector


class Camera:
    def __init__(self, index=0):
        self.video = cv2.VideoCapture(index)
        if not self.video.isOpened():
            raise RuntimeError("Cannot open cam")

    def read(self) -> numpy.ndarray | None:
        ret, frame = self.video.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.video.release()


class Tracker:
    def __init__(self, camera: Camera, detector: Detector):
        self.camera = camera
        self.detector = detector

        self.frames = queue.Queue(maxsize=3)
        self.results = queue.Queue(maxsize=3)
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.capture, daemon=True).start()
        threading.Thread(target=self.process, daemon=True).start()

    def capture(self):
        while self.running:
            frame = self.camera.read()
            if frame is None:
                continue

            try:
                self.frames.put(frame, timeout=0.1)
            except queue.Full:
                try:
                    self.frames.get_nowait()
                except queue.Empty:
                    pass
                self.frames.put(frame)

    def process(self):
        count = 0

        last = None
        while self.running:
            try:
                frame: numpy.ndarray = self.frames.get(timeout=0.1)
                count += 1
            except queue.Empty:
                continue

            if count % 3 == 0 or last is None:
                faces = self.detector.detect(frame)
                height, width, channels = frame.shape

                results = []
                for face in faces:
                    center = utils.center(face)
                    normalized = utils.normalize(
                        center, models.objects.Size(width, height))

                    horizontal = models.states.Horizontal.classify(
                        normalized.x)
                    vertical = models.states.Vertical.classify(normalized.y)

                    ratio = face.size.width / width
                    distance = models.states.Distance.classify(ratio)

                    result = models.dto.Result(
                        normalized, horizontal, vertical, distance)
                    results.append(result)
            else:
                faces, results = last

            try:
                self.results.put((frame, faces, results), timeout=0.1)
            except queue.Full:
                try:
                    self.results.get_nowait()
                except queue.Empty:
                    pass
                self.results.put((frame, faces, results), timeout=0.1)

            last = (faces, results)
