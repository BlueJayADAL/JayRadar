import cv2
from collections import deque
import threading


class ThreadedCamera:
    def __init__(self, device:int=0, buffer:int=5):
        """
        Initialize the ThreadedCamera object.

        Args:
            device (int): Index of the camera device to use. Defaults to 0.
            buffer (int): Maximum number of frames to store in the output queue. Defaults to 5.
        """
        # Assuming camera index 0
        self._device = device
        self._dq_out = deque(maxlen=buffer)  # Output queue to store frames
        self._active = False  # Flag to indicate if capturing is active

    def _record_frames(self):
        """
        Internal method to capture frames from the camera and put them in the output queue.
        This method runs in a separate thread.
        """
        # Set the active flag to True
        self._active = True

        # Open the camera
        _camera = cv2.VideoCapture(self._device)

        while self._active:
            # Read a frame from the camera
            ret, frame = _camera.read()

            if not ret:
                break

            # Put the frame into the output queue
            self._dq_out.append(frame)

        # Release the camera
        _camera.release()

        # Signal the end of frames by putting None in the output queue
        self._dq_out.append(None)

    def start_capture(self):
        """
        Start capturing frames from the camera by creating a new thread.
        """
        # Create a new thread to capture frames
        self._capture_thread = threading.Thread(target=self._record_frames)
        self._capture_thread.start()

    def stop_capture(self):
        """
        Stop capturing frames from the camera by setting the active flag to False.
        """
        # Set the active flag to False, stopping the frame capturing
        self._active = False

    def get_frame(self):
        """
        Get the latest captured frame from the output queue.

        Returns:
            numpy.ndarray or None: The latest frame if available, otherwise None.
        """
        if self._dq_out:
            # Return the latest frame from the output queue
            frame = self._dq_out[-1]
            return frame
        else:
            return None
