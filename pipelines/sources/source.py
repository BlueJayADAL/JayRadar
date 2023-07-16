import cv2
import time

class Source:
    def __init__(self, device:int=0, windows:bool = False):
        self.device = device
        self.windows = windows
        self.running = False

    def initialize(self):
        if self.windows:
            self.cap = cv2.VideoCapture(self.device, cv2.CAP_DSHOW)
        else:
            self.cap = self.cap = cv2.VideoCapture(self.device)

    def get_frame(self):
        data={"timestamp": time.time()}

        ret, frame = self.cap.read()
        if ret:
            return frame, data
        else:
            return None, data
    
    def release(self):
        self.cap.release()