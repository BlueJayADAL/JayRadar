import threading
import cv2
from capture import capture_frames
from process import process_frames
from send import send_frames

# Start the capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

# Start the processing thread
process_thread = threading.Thread(target=process_frames)
process_thread.start()

# Start the frame sending thread
send_thread = threading.Thread(target=send_frames)
send_thread.start()

# Wait for threads to finish
capture_thread.join()
process_thread.join()
send_thread.join()

cv2.destroyAllWindows()
