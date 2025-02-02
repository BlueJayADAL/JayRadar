import cv2
import time
from networktables import NetworkTables
from multiprocessing import Queue
from .output import Output


class NTSend(Output):
    """
    NTSend class for q'ing frames and sending data to NetworkTables.

    This class is used push frames to a shared q and send additional data to NetworkTables.
    """  # noqa: E501

    def __init__(
        self,
        q_out: Queue,
        server: str = '10.1.32.27',
        table: str = 'JayRadar',
        verbose=False
    ):
        """
        Initialize the NTSend.

        Args:
            server (str): IP address of the NetworkTables server. Defaults to '10.1.32.27'.
            table (str): Name of the NetworkTable to use. Defaults to 'JayRadar'.
            verbose (bool): Set to True to enable verbose mode and print debug information. Defaults to False.
        """  # noqa: E501
        self.server = server  # IP address of the NetworkTables server
        self.table_name = table  # Name of the NetworkTable
        self.running = False  # Flag indicating if the NTDisplay is running
        self.verbose = verbose  # Flag indicating if verbose mode is enabled
        self.q_out = q_out

    def initialize(self):
        """
        Initialize NetworkTables.

        This method initializes the NetworkTables library and connects to the specified server.
        It also retrieves the NetworkTable to be used for data communication.
        """  # noqa: E501
        NetworkTables.initialize(
            server=self.server)  # Initialize NetworkTables
        self.table = NetworkTables.getTable(
            self.table_name)  # Get the specified NetworkTable

    def send_frame(self, frame, data):
        """
        Send additional data to NetworkTables, make frame available in q.

        Args:
            frame (numpy.ndarray): The frame to be displayed in the OpenCV window.
            data (dict): A dictionary containing additional data to be sent to NetworkTables.
                         It must contain a 'timestamp' key with the timestamp of the frame.

        This method puts the additional data in the NetworkTable, such as the timestamp,
        end-to-end time, and frames per second. It also pushes the frame to the q.
        """  # noqa: E501
        for key, value in data.items():
            # Put each key-value pair in the NetworkTable
            self.table.putValue(key, value)
            if self.verbose:
                print(f"Placed on table: /{self.table_name}/{key}/{value}")

        self.q_out.put(frame)
        final_time = time.time()

        # Calculate end-to-end time
        end_to_end_time = round(final_time - data["timestamp"], 5)
        if end_to_end_time < .0001:
            end_to_end_time = .0001

        # Put end-to-end time in the NetworkTable
        self.table.putNumber("IterationTime", end_to_end_time)
        # Put frames per second in the NetworkTable
        self.table.putNumber("FPS", (1/end_to_end_time))

        if self.verbose:
            print(
                f"End to end time: {end_to_end_time} | "
                f"FPS: {1/end_to_end_time}")

    def release(self):
        """
        Release the OpenCV window.

        This method closes the OpenCV window used for displaying frames.
        """  # noqa: E501
        cv2.destroyAllWindows()  # Close the OpenCV window
