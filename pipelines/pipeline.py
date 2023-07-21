import cv2
from .pipes import Pipe
from .outputs import Output
from .sources import Source


class Pipeline:
    """
    Pipeline class for processing frames through a series of pipes and sending the output to an output handler.

    This class facilitates the processing of frames through a pipeline of pipes and sends the output to an
    output handler for display or further processing.
    """  # noqa: E501

    def __init__(self, source: Source, output: Output, *pipes: Pipe):
        """
        Initialize the Pipeline object.

        Args:
            source: An object providing frames for the pipeline.
            output: An object handling the output of the pipeline.
            *pipes: Variable-length argument list of pipe objects to process frames.

        The Pipeline object requires a source object, an output object, and a list of pipe objects.
        The pipes will be applied to the frames in the order they are provided.
        """  # noqa: E501
        self.source = source  # Object providing frames for the pipeline
        self.output = output  # Object handling the output of the pipeline
        self.pipes = pipes  # List of pipe objects to process frames
        self.num_pipes = len(self.pipes)  # Number of pipes in the pipeline

    def initialize(self):
        """
        Initialize the Pipeline object.

        This method initializes the source, output, and each pipe in the pipeline by calling their
        respective initialize() methods. It then starts the pipeline by calling the run() method.
        """  # noqa: E501
        self.source.initialize()  # Initialize the source object
        self.output.initialize()  # Initialize the output object

        for pipe in self.pipes:
            pipe.initialize()  # Initialize each pipe in the pipeline

        self.run()  # Start processing frames through the pipeline

    def run(self):
        """
        Start processing frames through the pipeline.

        This method continuously processes frames received from the source through the pipes in the pipeline.
        The processed frames and associated data are sent to the output object using the send_frame() method.
        The loop terminates when the source returns None for the frame, indicating the end of frames.
        """  # noqa: E501
        while True:
            frame, data = self.source.get_frame()
            if frame is None:
                break

            for pipe in self.pipes:
                # Process the frame through each pipe
                frame, data = pipe.run_pipe(frame, data)

            # Send the processed frame and data to the output
            self.output.send_frame(frame, data)
            # Wait for a short period to display any CV2 Windows
            cv2.waitKey(1)

        self.cleanup()  # Perform cleanup after processing all frames

    def cleanup(self):
        """
        Cleanup resources used by the Pipeline object.

        This method releases resources used by the source, output, and each pipe in the pipeline by calling
        their respective release() methods.
        """  # noqa: E501
        self.source.release()  # Release resources used by the source object
        self.output.release()  # Release resources used by the output object

        for pipe in self.pipes:
            pipe.release()
