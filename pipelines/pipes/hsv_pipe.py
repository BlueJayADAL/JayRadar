import cv2
import numpy as np
from .pipe import Pipe


class HSVPipe(Pipe):
    """
    HSVPipe class for adjusting brightness, contrast, and saturation of an HSV frame.

    This class allows adjusting the brightness, contrast, and saturation of an HSV frame.
    """

    def __init__(self, config: dict = {"brightness": 0, "contrast": 1.0, "saturation": 1.0}):
        """
        Initialize the HSVPipe object.

        Args:
            config (dict): A dictionary specifying the amount of adjustment for brightness, contrast, and saturation.
                           It should contain three keys: 'brightness', 'contrast', and 'saturation'.
                           The values for 'brightness' should be an integer representing the amount of brightness
                           adjustment to be added to the V channel of the HSV frame.
                           The values for 'contrast' and 'saturation' should be floats representing the amount of
                           contrast and saturation adjustment to be applied to the V and S channels of the HSV frame,
                           respectively. Defaults to {"brightness": 0, "contrast": 1.0, "saturation": 1.0}.
        """
        self._config = config  # Dictionary containing the adjustment values for brightness, contrast, and saturation

    def run_pipe(self, frame, data):
        """
        Process an HSV frame by adjusting brightness, contrast, and saturation.

        Args:
            frame (numpy.ndarray): The HSV frame to be processed.
            data (dict): A dictionary containing additional data related to the frame.

        Returns:
            tuple: A tuple containing the processed frame and the data dictionary unchanged.

        This method adjusts the brightness, contrast, and saturation of the input HSV frame
        based on the specified adjustment values in the config dictionary. The brightness is
        added to the V channel, and the contrast and saturation are multiplied with the V and S
        channels, respectively. The values for V and S channels are clamped to the valid range [0, 255],
        and the channels are merged back to form the processed frame. The frame is then converted
        back to the BGR color space before returning.
        """
        frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2HSV)  # Convert the frame to HSV color space
        h, s, v = cv2.split(frame)  # Split the frame into individual channels

        # Adjust brightness
        v = cv2.add(v, self._config["brightness"])

        # Adjust contrast
        v = cv2.multiply(v, self._config["contrast"])

        # Adjust saturation
        s = cv2.multiply(s, self._config["saturation"])

        # Clamp values to valid range [0, 255]
        v = np.clip(v, 0, 255)
        s = np.clip(s, 0, 255)

        # Merge the channels back into an HSV frame
        frame = cv2.merge((h, s, v))
        # Convert the frame back to BGR color space
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        return frame, data  # Return the processed frame and the data dictionary unchanged
