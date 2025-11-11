
from src.buddy import Buddy
from src.buddy.core.communication import Arduino
from src.buddy.core.controllers import PID
from src.buddy.core.detectors import Cascade
from src.buddy.core.track import Camera, Tracker


if __name__ == "__main__":
    camera = Camera(0)
    detector = Cascade(0.5)
    tracker = Tracker(camera, detector)
    buddy = Buddy(tracker, Arduino(), PID(1, 0, 0, 0.5), PID(1, 0, 0, 0.5))
    buddy.run()
