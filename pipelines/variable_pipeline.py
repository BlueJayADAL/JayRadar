import cv2
from pipelines import Pipeline

class VariablePipeline(Pipeline):
    """
    VariablePipeline class for processing frames through a series of filters with the ability to modify filters at runtime.

    This class extends the base Pipeline class to allow adding and removing filters at runtime through a command queue.
    It provides additional methods for managing filters dynamically during the pipeline's execution.
    """

    def __init__(self, source, output, filter_q, *filters):
        """
        Initialize the VariablePipeline object.

        Args:
            source: An object providing frames for the pipeline.
            output: An object handling the output of the pipeline.
            filter_q: A queue for receiving commands to add or remove filters at runtime.
            *filters: Variable-length argument list of filter objects to process frames.

        The VariablePipeline object extends the base Pipeline object by adding the ability to modify filters at runtime.
        The filters will be applied to the frames in the order they are provided.
        """
        super().__init__(source, output, *filters)
        self.filters = list(self.filters)  # Convert the filters to a mutable list
        self.filter_q = filter_q  # Queue for receiving commands to add or remove filters
        self.check_q()  # Process any initial commands in the queue

    def check_q(self):
        """
        Check the filter queue for commands to add or remove filters at runtime.

        This method continuously checks the filter queue for incoming commands and processes them accordingly.
        Valid commands include "add" to add a new filter at a specified index and "delete" to remove a filter
        at a specified index. If the index is out of bounds, it will be adjusted to fit within the valid range.
        """
        while not self.filter_q.empty():
            command, index, filter = self.filter_q.get()

            if command == "add":
                self.add_filter(filter, index=index)
            elif command == "delete":
                self.del_filter(index)

    def add_filter(self, filter, index=0):
        """
        Add a new filter to the pipeline at the specified index.

        Args:
            filter: The filter object to be added.
            index (int): The index where the filter should be inserted. Defaults to 0.

        If the specified index is greater than the number of filters, the filter will be inserted at the end of the pipeline.
        The filter is initialized before being added to the pipeline, and the number of filters is updated accordingly.
        """
        if index > self.num_filters:
            index = self.num_filters
        filter.initialize()  # Initialize the new filter
        self.filters.insert(index, filter)  # Insert the new filter at the specified index
        self.num_filters += 1  # Increment the number of filters

    def del_filter(self, index:int=0):
        """
        Remove a filter from the pipeline at the specified index.

        Args:
            index (int): The index of the filter to be removed. Defaults to 0.

        Returns:
            bool: True if the filter is successfully removed, False if the index is out of bounds.

        If the specified index is greater than or equal to the number of filters, the method returns False.
        Otherwise, the filter at the specified index is removed from the pipeline, and the number of filters is updated.
        """
        if index > (self.num_filters-1):  # Check if the index is out of bounds
            return False
        else:
            del self.filters[index]  # Remove the filter at the specified index
            self.num_filters -= 1  # Decrement the number of filters
            return True

    def run(self):
        """
        Start processing frames through the pipeline.

        This method continuously processes frames received from the source through the filters in the pipeline.
        The processed frames and associated data are sent to the output object using the send_frame() method.
        The loop terminates when the source returns None for the frame, indicating the end of frames.
        The method also checks the filter queue for commands to modify filters at runtime.
        """
        while True:
            self.check_q()  # Check the filter queue for any commands

            frame, data = self.source.get_frame()  # Get a frame from the source
            if frame is None:
                break

            for filter in self.filters:
                frame, data = filter.process_frame(frame, data)  # Process the frame through each filter

            self.output.send_frame(frame, data)  # Send the processed frame and data to the output
            cv2.waitKey(1)  # Wait for a short period to handle GUI events

        self.cleanup()  # Perform cleanup after processing all frames
