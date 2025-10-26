import cv2
import queue
import threading

from src.buddy import configs, models


class Tracker:
    def __init__(self, window: models.Window):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise RuntimeError("Cannot open webcam")

        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.classifier = cv2.CascadeClassifier(path)

        self.window = window
        cv2.namedWindow(self.window.name, cv2.WINDOW_NORMAL)
        if self.window.fullscreen:
            cv2.setWindowProperty(
                self.window.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.frames = queue.Queue(maxsize=3)
        self.results = queue.Queue(maxsize=3)
        self.running = True

    def capture(self):
        while self.running:
            ret, frame = self.video.read()
            if not ret:
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
        scales = dict()

        last = None
        while self.running:
            try:
                frame = self.frames.get(timeout=0.1)
                count += 1
            except queue.Empty:
                continue

            if count % 3 == 0 or last is None:
                faces = self.detect(frame)
                results = []

                scales["x"] = frame.shape[1] / self.window.width
                scales["y"] = frame.shape[0] / self.window.height

                for face in faces:
                    x = int(face.position.x * scales["x"])
                    y = int(face.position.y * scales["y"])
                    w = int(face.width * scales["x"])
                    h = int(face.height * scales["y"])

                    center = models.Position(int(x + w / 2), int(y + h / 2))
                    normalized = models.Position(
                        center.x / frame.shape[1], center.y / frame.shape[0])

                    horizontal = "CENTER"
                    if normalized.x < configs.Thresholds.LEFT.value:
                        horizontal = "LEFT"
                    elif normalized.x > configs.Thresholds.RIGHT.value:
                        horizontal = "RIGHT"

                    vertical = "CENTER"
                    if normalized.y < configs.Thresholds.TOP.value:
                        vertical = "TOP"
                    elif normalized.y > configs.Thresholds.BOTTOM.value:
                        vertical = "BOTTOM"

                    ratio = w / frame.shape[1]
                    if ratio > 0.35:
                        distance = "Very Close"
                    elif ratio > 0.18:
                        distance = "Close"
                    elif ratio > 0.08:
                        distance = "Medium"
                    else:
                        distance = "Far"

                    result = models.Result(
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
                self.frames.put((frame, faces, results), timeout=0.1)

            last = (faces, results)

    def detect(self, frame):
        resized = cv2.resize(frame, (self.window.width, self.window.height))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        faces = []
        for (x, y, w, h) in self.classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)):
            faces.append(models.Face(models.Position(x, y), w, h))
        return faces

    def run(self):
        threads = [
            threading.Thread(target=self.capture),
            threading.Thread(target=self.process)
        ]
        for t in threads:
            t.start()

        while self.running:
            try:
                frame, faces, results = self.results.get(timeout=0.1)
            except queue.Empty:
                continue

            for face, result in zip(faces, results):
                face: models.Face
                result: models.Result

                x, y, w, h = int(face.position.x * (frame.shape[1]/self.window.width)), int(face.position.y * (frame.shape[0]/self.window.height)), int(
                    face.width * (frame.shape[1]/self.window.width)), int(face.height * (frame.shape[0]/self.window.height))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                label = f"{result.horizontal}/{result.vertical} | nx={result.normalized.x:.2f}, ny={result.normalized.y:.2f} | {result.distance}"
                cv2.putText(frame, label, (x, max(y-10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow(self.window.name, frame)
            if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
                self.running = False
                break

        for t in threads:
            t.join()
        self.video.release()
        cv2.destroyAllWindows()
