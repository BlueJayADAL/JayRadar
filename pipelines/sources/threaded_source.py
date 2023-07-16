import cv2
from collections import deque
import threading
import time

class ThreadedSource:
    def __init__(self, device:int=0, windows:bool = False, buffer:int = 5):
        self._device = device
        self._dq_out = deque(maxlen=buffer)
        self._active = False
        self.windows = windows

    def initialize(self):
        if self.windows:
            self._camera = cv2.VideoCapture(self._device, cv2.CAP_DSHOW)
        else:
            self._camera = cv2.VideoCapture(self._device)
        self.start()
        

    def _record_frames(self):
        self._active = True
        while self._active:
            ret, frame = self._camera.read()

            if not ret:
                break

            time_stamp = time.time()
            
            self._dq_out.append([frame, time_stamp])

        self._camera.release()
        self._dq_out.append([None, None])

    def start(self):
        self._capture_thread = threading.Thread(target=self._record_frames)
        self._capture_thread.start()

    def get_frame(self):
        if not self._active:
            self.start()
            self.running = True

        if self._dq_out:
            data = self._dq_out[-1]
            return data[0], {"timestamp":data[1]}
        elif self._active:
            time.sleep(1)
            return self.get_frame()
        else:
            return None, None
    def release(self):
        self._active = False
        