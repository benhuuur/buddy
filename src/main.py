from src.buddy import Tracker
from src.buddy.models import Window

if __name__ == "__main__":
    window = Window("Face Tracker", 320, 240, True)
    tracker = Tracker(window)
    tracker.run()
