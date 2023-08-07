import cv2
import time


class Output:
    """
    Output class for displaying frames using OpenCV.

    This class is used to display frames in an OpenCV window and print end-to-end time and frames per second (FPS).
    """  # noqa: E501

    def __init__(self):
        """
        Initialize the Output object.

        This class does not require any initialization or parameters.
        """  # noqa: E501
        pass

    def initialize(self):
        """
        Initialize the Output object.

        This method is currently empty as the Output class does not require any initialization.
        """  # noqa: E501
        pass

    def send_frame(self, frame, data):
        """
        Display a frame and print end-to-end time and FPS.

        Args:
            frame (numpy.ndarray): The frame to be displayed in the OpenCV window.
            data (dict): A dictionary containing additional data related to the frame.
                         It must contain a 'timestamp' key with the timestamp of the frame.

        This method displays the frame in an OpenCV window and calculates the end-to-end time
        (time elapsed from frame capture to display) and FPS (frames per second).
        """  # noqa: E501
        cv2.imshow('Output', frame)  # Display the frame in an OpenCV window
        final_time = time.time()

        # Calculate end-to-end time
        end_to_end_time = round(final_time - data["timestamp"], 5)
        if end_to_end_time < .0001:
            end_to_end_time = .0001

        # Print end-to-end time and FPS
        print(f"End to end time: {end_to_end_time} | FPS: {1/end_to_end_time}")

    def release(self):
        """
        Release the OpenCV window.

        This method closes the OpenCV window used for displaying frames.
        """  # noqa: E501
        cv2.destroyAllWindows()  # Close the OpenCV window
