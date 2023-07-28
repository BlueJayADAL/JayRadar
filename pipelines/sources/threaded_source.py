import cv2
from collections import deque
import threading
import time
from .source import Source


class ThreadedSource(Source):
    """
    ThreadedSource class for capturing frames from a video source using OpenCV in a separate thread.

    This class allows capturing frames from a camera device or a video file, using a threaded approach
    for improved performance and responsiveness.
    """  # noqa: E501

    def __init__(
        self,
        device: int = 0,
        windows: bool = False,
        buffer: int = 5
    ):
        """
        Initialize the ThreadedSource object.

        Args:
            device (int): Index of the camera device to use or the path to the video file.
                          Defaults to 0, which corresponds to the default camera.
            windows (bool): Set to True if running on Windows and capturing from the default camera.
                            Defaults to False.
            buffer (int): Maximum number of frames to store in the output queue. Defaults to 5.
        """  # noqa: E501
        self._device = device  # Camera device index or video file path
        # Output queue to store frames and timestamps
        self._dq_out = deque(maxlen=buffer)
        self._active = False  # Flag indicating if the thread is active
        self.windows = windows  # Flag indicating if running on Windows

    def initialize(self):
        """
        Initialize the threaded video capture.

        This method creates a VideoCapture object using the specified device index or video file path.
        If running on Windows and capturing from the default camera, it uses CAP_DSHOW to avoid issues.
        It also starts the thread for capturing frames in the background.
        """  # noqa: E501
        if self.windows:
            self._camera = cv2.VideoCapture(self._device, cv2.CAP_DSHOW)
        else:
            self._camera = cv2.VideoCapture(self._device)

        self.start()  # Start capturing frames in the background

    def _record_frames(self):
        """
        Internal method to capture frames from the video source and put them in the output queue.
        This method runs in a separate thread.
        """  # noqa: E501
        self._active = True

        while self._active:
            ret, frame = self._camera.read()

            if not ret:
                break

            time_stamp = time.time()

            # Append the frame and timestamp to the output queue
            self._dq_out.append([frame, time_stamp])

        self._camera.release()  # Release the video source
        # Signal the end of frames by putting None in the output queue
        self._dq_out.append([None, None])

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
        """  # noqa: E501
        if self._dq_out:
            # Get the latest captured frame and timestamp from the output queue
            data = self._dq_out[-1]
            # Return the frame and the timestamp as additional data
            return data[0], {"timestamp": data[1]}
        elif self._active:
            time.sleep(1)  # Sleep briefly to avoid busy waiting
            return self.get_frame()
        else:
            return None, None

    def release(self):
        """
        Stop capturing frames and release the video source.

        This method stops the threaded source by setting the active flag to False.
        """  # noqa: E501
        self._active = False
