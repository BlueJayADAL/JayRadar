class ExampleFilter:
    """
    ExampleFilter class for filtering frames.

    This class demonstrates the structure of a basic filter class used for processing frames.
    """

    def __init__(self, config:dict={"example": 0}):
        """
        Initialize the ExampleFilter object.

        Args:
            config (dict): A dictionary specifying configuration parameters for the filter.
                           Defaults to {"example": 0}.
        """
        # Only use this to save the input, do not initialize objects here.
        # Variables initialized here will have to be sent to the new process
        self.config = config

    def initialize(self):
        """
        Initialize the ExampleFilter object.

        Use this method to initialize objects or perform any setup required for the filter.
        This will be called once a new process is started.
        """
        pass

    def process_frame(self, frame, data):
        """
        Process a frame and associated data.

        Args:
            frame (any): The frame to be processed. The data type can be specific to the use case.
            data (any): Additional data related to the frame. The data type can be specific to the use case.

        Returns:
            tuple: A tuple containing the processed frame and the processed data.

        This method processes the input frame and data according to the logic specific to the filter.
        It can perform various operations on the frame and modify the data as needed.
        The processed frame and data are returned in a tuple for further processing or display.
        """
        # Do something to the frame and data.
        # The actual processing logic will depend on the filter's specific use case.
        return frame, data

    def release(self):
        """
        Release resources used by the ExampleFilter object.

        This method is currently empty as the ExampleFilter class does not require any resource release.
        """
        pass
