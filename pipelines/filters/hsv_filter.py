import cv2
import numpy as np

class HSVFilter:
    def __init__(self, config:dict={"brightness": 0, "contrast": 1.0, "saturation": 1.0}):
        self.config = config

    def initialize(self):
        pass

    def process_frame(self, frame, data):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(frame)

        # Adjust brightness
        v = cv2.add(v, self.config["brightness"])

        # Adjust contrast
        v = cv2.multiply(v, self.config["contrast"])

        # Adjust saturation
        s = cv2.multiply(s, self.config["saturation"])

        # Clamp values to valid range
        v = np.clip(v, 0, 255)
        s = np.clip(s, 0, 255)

        frame = cv2.merge((h, s, v))
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        return frame, data

    def release(self):
        pass