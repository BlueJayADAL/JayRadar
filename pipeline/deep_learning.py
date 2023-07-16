from ultralytics import YOLO
from pipeline.cameras import ThreadedCamera
import cv2

class DeepLearning():
    def __init__(self):
        """
        Initialize the DeepLearning object.

        This class is responsible for running a deep learning pipeline using YOLO model and a threaded camera.
        """
        self.model = YOLO('yolov8n.pt')  # YOLO model for object detection
        self.camera = ThreadedCamera()  # Threaded camera for capturing frames
        self.active = False  # Flag to indicate if the pipeline is active

    def stop_pipeline(self):
        """
        Stop the deep learning pipeline.
        """
        self.active = False
    
    def run_pipeline(self):
        """
        Run the deep learning pipeline.

        This method starts the camera capture, performs object detection on each frame,
        and displays the annotated frames in a window until the 'q' key is pressed.
        """
        self.camera.start_capture()  # Start camera capture
        self.active = True  # Set the pipeline as active

        while self.active:

            frame = self.camera.get_frame()  # Get the latest captured frame

            if frame is not None:

                results = self.model.predict(frame, verbose=False)  # Perform object detection on the frame

                annotated_frame = results[0].plot()  # Annotate the frame with detected objects

                cv2.imshow("Deep Learning", annotated_frame)  # Display the annotated frame in a window

                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):  # Break the loop if 'q' key is pressed
                    break

        cv2.destroyAllWindows()  # Close the display window
        self.camera.stop_capture()  # Stop camera capture
