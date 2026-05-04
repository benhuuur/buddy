from src.buddy import Buddy
from src.buddy.core.controllers import PID
from src.buddy.core.detectors import Cascade
from src.buddy.core.track import Camera, Tracker
from src.buddy.core.communication import Arduino


if __name__ == "__main__":
    camera = Camera(1)
    detector = Cascade(0.5)
    tracker = Tracker(camera, detector)
    buddy = Buddy(tracker, Arduino(), PID(1, 0, 0, 0.5), PID(1, 0, 0, 0.5))
    # buddy = Buddy(tracker, Arduino(), PID(5.5, 10, 1.20, 0.5), PID(4, 0, 0, 0.5))
    buddy.run()
