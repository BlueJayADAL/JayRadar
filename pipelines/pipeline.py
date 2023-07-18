import cv2

class Pipeline:
    """
    Pipeline class for processing frames through a series of filters and sending the output to an output handler.

    This class facilitates the processing of frames through a pipeline of filters and sends the output to an
    output handler for display or further processing.
    """

    def __init__(self, source, output, *filters):
        """
        Initialize the Pipeline object.

        Args:
            source: An object providing frames for the pipeline.
            output: An object handling the output of the pipeline.
            *filters: Variable-length argument list of filter objects to process frames.

        The Pipeline object requires a source object, an output object, and a list of filter objects.
        The filters will be applied to the frames in the order they are provided.
        """
        self.source = source  # Object providing frames for the pipeline
        self.output = output  # Object handling the output of the pipeline
        self.filters = filters  # List of filter objects to process frames
        self.num_filters = len(self.filters)  # Number of filters in the pipeline

    def initialize(self):
        """
        Initialize the Pipeline object.

        This method initializes the source, output, and each filter in the pipeline by calling their
        respective initialize() methods. It then starts the pipeline by calling the run() method.
        """
        self.source.initialize()  # Initialize the source object
        self.output.initialize()  # Initialize the output object

        for pipe in self.filters:
            pipe.initialize()  # Initialize each filter in the pipeline

        self.run()  # Start processing frames through the pipeline

    def run(self):
        """
        Start processing frames through the pipeline.

        This method continuously processes frames received from the source through the filters in the pipeline.
        The processed frames and associated data are sent to the output object using the send_frame() method.
        The loop terminates when the source returns None for the frame, indicating the end of frames.
        """
        while True:
            frame, data = self.source.get_frame()  # Get a frame from the source
            if frame is None:
                break

            for filter in self.filters:
                frame, data = filter.process_frame(frame, data)  # Process the frame through each filter

            self.output.send_frame(frame, data)  # Send the processed frame and data to the output
            cv2.waitKey(1)  # Wait for a short period to display any CV2 Windows

        self.cleanup()  # Perform cleanup after processing all frames

    def cleanup(self):
        """
        Cleanup resources used by the Pipeline object.

        This method releases resources used by the source, output, and each filter in the pipeline by calling
        their respective release() methods.
        """
        self.source.release()  # Release resources used by the source object
        self.output.release()  # Release resources used by the output object

        for pipe in self.filters:
            pipe.release()  # Release resources used by each filter in the pipeline
