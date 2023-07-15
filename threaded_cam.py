import cv2
from collections import deque
import threading


class ThreadedCamera:
    def __init__(self, device:int=1, buffer:int=5):
        self._camera = cv2.VideoCapture(device, cv2.CAP_DSHOW)  # Assuming camera index 0
        self._dq_out = deque(maxlen=buffer)
        self._active = False


    def _record_frames(self):
        
        self._active = True

        while self._active:
            ret, frame = self._camera.read()

            if not ret:
                break

            # Put the frame into the output queue
            self._dq_out.append(frame)

        # Release the camera
        self._camera.release()

        # Signal the end of frames by putting None in the output queue
        self._dq_out.append(None)

    def start_capture(self):
        self._capture_thread = threading.Thread(target=self._record_frames)
        self._capture_thread.start()

    def stop_capture(self):
        self._active = False

    def get_frame(self):
        if self._dq_out:
            frame = self._dq_out[-1]
            return frame
        else:
            return None