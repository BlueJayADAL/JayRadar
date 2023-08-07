import cv2
from multiprocessing import Queue
from .pipeline import Pipeline
from .sources import Source
from .outputs import Output
from .pipes import Pipe


class VariablePipeline(Pipeline):
    """
    VariablePipeline class for processing frames through a series of pipes with the ability to modify pipes at runtime.

    This class extends the base Pipeline class to allow adding and removing pipes at runtime through a command queue.
    It provides additional methods for managing pipes dynamically during the pipeline's execution.
    """  # noqa: E501

    def __init__(
        self,
        source: Source,
        output: Output,
        pipe_q: Queue,
        *pipes: Pipe
    ):
        """
        Initialize the VariablePipeline object.

        Args:
            source: An object providing frames for the pipeline.
            output: An object handling the output of the pipeline.
            pipe_q: A queue for receiving commands to add or remove pipes at runtime.
            *pipes: Variable-length argument list of pipe objects to process frames.

        The VariablePipeline object extends the base Pipeline object by adding the ability to modify pipes at runtime.
        The pipes will be applied to the frames in the order they are provided.
        """  # noqa: E501
        super().__init__(source, output, *pipes)
        # Convert the pipes to a mutable list
        self.pipes = list(self.pipes)
        self.pipe_q = pipe_q
        self.check_q()  # Process any initial commands in the queue

    def check_q(self):
        """
        Check the pipe queue for commands to add or remove pipes at runtime.

        This method continuously checks the pipe queue for incoming commands and processes them accordingly.
        Valid commands include "add" to add a new pipe at a specified index and "delete" to remove a pipe
        at a specified index. If the index is out of bounds, it will be adjusted to fit within the valid range.
        """  # noqa: E501
        while not self.pipe_q.empty():
            command, index, pipe = self.pipe_q.get()

            if command == "add":
                self.add_pipe(pipe, index)
            elif command == "delete":
                self.del_pipe(index)
            elif command == "move":
                self.move_pipe(index, pipe)

    def move_pipe(self, current_index, new_index):
        pipe = self.pipes.pop(current_index)
        self.pipes.insert(new_index, pipe)

    def add_pipe(self, pipe, index=0):
        """
        Add a new pipe to the pipeline at the specified index.

        Args:
            pipe: The pipe object to be added.
            index (int): The index where the pipe should be inserted. Defaults to 0.

        If the specified index is greater than the number of pipes, the pipe will be inserted at the end of the pipeline.
        The pipe is initialized before being added to the pipeline, and the number of pipes is updated accordingly.
        """  # noqa: E501
        if index > self.num_pipes:
            index = self.num_pipes
        pipe.initialize()  # Initialize the new pipe
        # Insert the new pipe at the specified index
        self.pipes.insert(index, pipe)
        self.num_pipes += 1  # Increment the number of pipes

    def del_pipe(self, index: int = 0):
        """
        Remove a pipe from the pipeline at the specified index.

        Args:
            index (int): The index of the pipe to be removed. Defaults to 0.

        If the specified index is greater than or equal to the number of pipes, the method does nothing.
        Otherwise, the pipe at the specified index is removed from the pipeline, and the number of pipes is updated.
        """  # noqa: E501
        if index > (self.num_pipes-1):  # Check if the index is out of bounds
            pass
        else:
            del self.pipes[index]  # Remove the pipe at the specified index
            self.num_pipes -= 1  # Decrement the number of pipes

    def run(self):
        """
        Start processing frames through the pipeline.

        This method continuously processes frames received from the source through the pipes in the pipeline.
        The processed frames and associated data are sent to the output object using the send_frame() method.
        The loop terminates when the source returns None for the frame, indicating the end of frames.
        The method also checks the pipe queue for commands to modify pipes at runtime.
        """  # noqa: E501
        while True:
            self.check_q()  # Check the pipe queue for any commands

            frame, data = self.source.get_frame()
            if frame is None:
                break

            for pipe in self.pipes:
                # Process the frame through each pipe
                frame, data = pipe.run_pipe(frame, data)

            # Send the processed frame and data to the output
            self.output.send_frame(frame, data)
            cv2.waitKey(1)  # Wait for a short period to handle GUI events

        self.cleanup()  # Perform cleanup after processing all frames
