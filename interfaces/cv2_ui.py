from pipelines import PipelineManager
from multiprocessing import Queue
import cv2

class CV2UI:
    """
    CV2UI class for providing a terminal-based user interface to interact with a video processing pipeline.

    This class allows the user to view frames from the video processing pipeline in a window using OpenCV and
    interact with the pipeline by pressing keys on the keyboard. The available commands are:
    - Press "q" to quit the application.
    - Press "d" to delete the first filter in the pipeline.
    - Press "y" to add a DeepLearning filter at the beginning of the pipeline.

    The user can interact with the pipeline managed by a PipelineManager object using this terminal user interface.
    """

    def __init__(self, manager: PipelineManager, q_in: Queue):
        """
        Initialize the CV2UI object.

        Args:
            manager (PipelineManager): The PipelineManager object used to manage the video processing pipeline.
            q_in (Queue): The multiprocessing Queue to receive frames from the video processing pipeline.
        """
        self.manager = manager
        self.q_in = q_in

    def run(self):
        """
        Run the terminal user interface.

        The method provides a loop where the user can view frames from the video processing pipeline in a window using
        OpenCV and interact with the pipeline by pressing keys on the keyboard. The available commands are:
        - Press "q" to quit the application.
        - Press "d" to delete the first filter in the pipeline.
        - Press "y" to add a DeepLearning filter at the beginning of the pipeline.

        The method continuously retrieves frames from the multiprocessing Queue and displays them in the "CV2 UI" window.
        It waits for keyboard input and executes the corresponding actions based on the pressed keys. The application
        will continue running until the user presses "q" to quit.

        After exiting the loop, the method releases the resources used by the pipeline manager and terminates the
        associated pipeline process.
        """
        while True:
            frame = self.q_in.get()

            if frame is not None:
                cv2.imshow("CV2 UI", frame)
            
            key = cv2.waitKey(1)

            if key == ord("q"):
                break
            elif key == ord("d"):
                self.manager.delete_index(0)
            elif key == ord("y"):
                self.manager.add_dl(0)
            elif key == ord("w"):
                self.manager.delete_filter("dl")

        self.release()

    def release(self):
        """
        Release resources and terminate the pipeline manager.

        The method releases the resources used by the pipeline manager and terminates the associated pipeline process.
        """
        self.manager.release()
