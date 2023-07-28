import cv2
import time


class Source:
    """
    Source class for capturing frames from a video source using OpenCV.

    This class allows capturing frames from a camera device or a video file.
    """

    def __init__(self, device: int = 0, windows: bool = False):
        """
        Initialize the Source object.

        Args:
            device (int): Index of the camera device to use or the path to the video file.
                          Defaults to 0, which corresponds to the default camera.
            windows (bool): Set to True if running on Windows and capturing from the default camera.
                            Defaults to False.
        """  # noqa: E501
        self.device = device  # Camera device index or video file path
        self.windows = windows  # Flag indicating if running on Windows
        self.running = False  # Flag indicating if the source is running

    def initialize(self):
        """
        Initialize the video capture.

        This method creates a VideoCapture object using the specified device index or video file path.
        If running on Windows and capturing from the default camera, it uses CAP_DSHOW to avoid issues.
        """  # noqa: E501
        if self.windows:
            self.cap = cv2.VideoCapture(self.device, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(self.device)

    def get_frame(self):
        """
        Get a frame from the video source.

        Returns:
            tuple: A tuple containing the frame and a dictionary with additional data.
            If a frame is successfully read, the tuple is (frame, data).
            If there's an error or no frame is available, the tuple is (None, data).
            The data dictionary contains the timestamp of when the frame was captured.
        """  # noqa: E501
        data = {"timestamp": time.time()}

        ret, frame = self.cap.read()
        if ret:
            return frame, data
        else:
            return None, data

    def release(self):
        """
        Release the video source.

        This method releases the VideoCapture object, freeing up the video source.
        """  # noqa: E501
        self.cap.release()  # Release the VideoCapture object
