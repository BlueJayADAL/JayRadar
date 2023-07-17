import cv2
from collections import deque
import threading
import time

class ThreadedSource:
    """
    ThreadedSource class for capturing frames from a video source using OpenCV in a separate thread.

    This class allows capturing frames from a camera device or a video file, using a threaded approach
    for improved performance and responsiveness.
    """

    def __init__(self, device:int=0, windows:bool = False, buffer:int = 5):
        """
        Initialize the ThreadedSource object.

        Args:
            device (int): Index of the camera device to use or the path to the video file.
                          Defaults to 0, which corresponds to the default camera.
            windows (bool): Set to True if running on Windows and capturing from the default camera.
                            Defaults to False.
            buffer (int): Maximum number of frames to store in the output queue. Defaults to 5.
        """
        self._device = device  # Camera device index or video file path
        self._dq_out = deque(maxlen=buffer)  # Output queue to store frames and timestamps
        self._active = False  # Flag indicating if the threaded source is active
        self.windows = windows  # Flag indicating if running on Windows

    def initialize(self):
        """
        Initialize the threaded video capture.

        This method creates a VideoCapture object using the specified device index or video file path.
        If running on Windows and capturing from the default camera, it uses CAP_DSHOW to avoid issues.
        It also starts the thread for capturing frames in the background.
        """
        if self.windows:
            self._camera = cv2.VideoCapture(self._device, cv2.CAP_DSHOW)
        else:
            self._camera = cv2.VideoCapture(self._device)

        self.start()  # Start capturing frames in the background

    def _record_frames(self):
        """
        Internal method to capture frames from the video source and put them in the output queue.
        This method runs in a separate thread.
        """
        self._active = True

        while self._active:
            ret, frame = self._camera.read()  # Read a frame from the video source

            if not ret:
                break

            time_stamp = time.time()  # Record the timestamp of when the frame was captured

            self._dq_out.append([frame, time_stamp])  # Append the frame and timestamp to the output queue

        self._camera.release()  # Release the video source
        self._dq_out.append([None, None])  # Signal the end of frames by putting None in the output queue

    def start(self):
        """
        Start capturing frames from the video source in a separate thread.
        """
        self._capture_thread = threading.Thread(target=self._record_frames)
        self._capture_thread.start()

    def get_frame(self):
        """
        Get a frame from the video source.

        Returns:
            tuple: A tuple containing the frame and a dictionary with additional data.
            If a frame is successfully read, the tuple is (frame, data), where
                - frame (numpy.ndarray): The captured frame.
                - data (dict): A dictionary containing the timestamp of when the frame was captured.
            If there's an error or no frame is available, the tuple is (None, None).
        """
        if self._dq_out:
            data = self._dq_out[-1]  # Get the latest captured frame and timestamp from the output queue
            return data[0], {"timestamp": data[1]}  # Return the frame and the timestamp as additional data
        elif self._active:
            time.sleep(1)  # Sleep briefly to avoid busy waiting
            return self.get_frame()  # Recursively call get_frame until a frame is available or the source stops
        else:
            return None, None  # Return None if there's an error or the threaded source has stopped

    def release(self):
        """
        Stop capturing frames and release the video source.

        This method stops the threaded source by setting the active flag to False.
        """
        self._active = False  # Set the active flag to False, stopping the threaded source
