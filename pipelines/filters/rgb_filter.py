import cv2
import numpy as np

class RGBFilter:
    def __init__(self, config:dict={"red": 0, "green": 0, "blue": 0}):
        self._config = config

    def initialize(self):
        pass

    def process_frame(self, frame, data):
        # Split the frame into individual channels
        b, g, r = cv2.split(frame)

        # Adjust red balance
        r = cv2.add(r, self._config["red"])

        # Adjust green balance
        g = cv2.add(g, self._config["green"])

        # Adjust blue balance
        b = cv2.add(b, self._config["blue"])

        # Clamp values to valid range
        r = np.clip(r, 0, 255)
        g = np.clip(g, 0, 255)
        b = np.clip(b, 0, 255)

        # Merge the channels back into a frame
        frame = cv2.merge((b, g, r))
        return frame, data

    def release(self):
        pass
