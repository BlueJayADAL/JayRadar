import cv2
import threading
from collections import deque

# Maximum number of frames to keep in the deque
MAX_FRAMES = 5

# Deque to share frames between threads
frame_queue = deque(maxlen=MAX_FRAMES)

# Event to control frame processing
process_event = threading.Event()

# Thread function to capture video frames and add them to the frame queue
def capture_frames():
    """
    Function to capture video frames and add them to the frame queue.
    """
    cap = cv2.VideoCapture(0)

    print("Camera Aquired")

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            # Put frame in the deque for processing
            frame_queue.append(frame)
            process_event.set()  # Set the event to resume frame processing

    cap.release()
