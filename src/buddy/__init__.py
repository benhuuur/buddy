import cv2
import queue

from src.buddy import models
from src.buddy.core.track import Tracker
from src.buddy.core.controllers import Controller


class Buddy:
    def __init__(self, tracker: Tracker, microcontroller, pan: Controller, tilt: Controller):
        self.tracker = tracker
        self.microcontroller = microcontroller
        self.pan = pan
        self.tilt = tilt
        self.running = False

    def run(self, draw: bool = True):
        self.tracker.start()
        self.running = True

        while self.running:
            try:
                frame, faces, results = self.tracker.results.get(timeout=0.1)
            except queue.Empty:
                continue

            for face, result in zip(faces, results):
                self.control(result)
                if draw:
                    self.draw(frame, face, result)

            cv2.imshow("Buddy", frame)
            cv2.namedWindow("Buddy", cv2.WINDOW_FULLSCREEN)
            if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
                self.stop()

        cv2.destroyAllWindows()

    def control(self, result: models.dto.Result):
        
        self.microcontroller.send(
            f"{-1*self.pan.compute(result.normalized.x)};{-1*self.tilt.compute(result.normalized.y)}"
        )

    def draw(self, frame, face: models.objects.Rectangle, result: models.dto.Result):
        cv2.rectangle(
            frame,
            (int(face.position.x), int(face.position.y)),
            (int(face.position.x + face.size.width),
             int(face.position.y + face.size.height)),
            (0, 255, 0),
            2
        )
        label = f"{result.horizontal}/{result.vertical} | nx={result.normalized.x:.2f}, ny={result.normalized.y:.2f} | {result.distance}"
        cv2.putText(
            frame,
            label,
            (int(face.position.x), int(max(face.position.y - 10, 20))),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    def stop(self):
        self.running = False
        self.tracker.running = False
        self.tracker.camera.release()
