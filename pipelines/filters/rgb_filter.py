import cv2
import numpy as np

class RGBFilter:
    """
    RGBFilter class for adjusting the red, green, and blue balance of an RGB frame.

    This class allows adjusting the color balance of an RGB frame by adding user-defined values to the
    red, green, and blue channels separately.
    """

    def __init__(self, config:dict={"red": 0, "green": 0, "blue": 0}):
        """
        Initialize the RGBFilter object.

        Args:
            config (dict): A dictionary specifying the amount of adjustment for each color channel.
                           It should contain three keys: 'red', 'green', and 'blue'.
                           The values for each channel should be integers representing the amount of
                           adjustment to be added to the respective channel. Defaults to {"red": 0, "green": 0, "blue": 0}.
        """
        self._config = config  # Dictionary containing the adjustment values for each channel

    def initialize(self):
        """
        Initialize the RGBFilter object.

        This method is currently empty as the RGBFilter class does not require any initialization.
        """
        pass

    def process_frame(self, frame, data):
        """
        Process a frame by adjusting the RGB balance.

        Args:
            frame (numpy.ndarray): The RGB frame to be processed.
            data (dict): A dictionary containing additional data related to the frame.

        Returns:
            tuple: A tuple containing the processed frame and the data dictionary unchanged.

        This method adjusts the color balance of the input RGB frame by adding the specified adjustment
        values to the red, green, and blue channels separately. The values for each channel are clamped
        to the valid range [0, 255], and the channels are merged back to form the processed frame.
        """
        # Split the frame into individual channels
        b, g, r = cv2.split(frame)

        # Adjust red balance
        r = cv2.add(r, self._config["red"])

        # Adjust green balance
        g = cv2.add(g, self._config["green"])

        # Adjust blue balance
        b = cv2.add(b, self._config["blue"])

        # Clamp values to valid range [0, 255]
        r = np.clip(r, 0, 255)
        g = np.clip(g, 0, 255)
        b = np.clip(b, 0, 255)

        # Merge the channels back into a frame
        frame = cv2.merge((b, g, r))
        return frame, data

    def release(self):
        """
        Release resources used by the RGBFilter object.

        This method is currently empty as the RGBFilter class does not require any resource release.
        """
        pass
