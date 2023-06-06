import cv2
from ultralytics import YOLO
import threading
import queue

# Queue to share frames between threads
frame_queue = queue.Queue()

# Thread function to capture video frames
def capture_frames():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            frame_queue.put(frame)
        else:
            break
    cap.release()

# Thread function to process frames with YOLOv8
def process_frames():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    while True:
        frame = frame_queue.get()
        # Run YOLOv8 inference on the frame
        results = model.predict(frame)
        for result in results:
            boxes = result.boxes # get boxes on cpu in numpy
            for box in boxes: # iterate boxes
                x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
                print(f"Coordinates: ({x1},{y1}) + ({x2},{y2})") # print boxes
                #cv2.rectangle(frame, r[:2], r[2:], (0,255,0), 2) # draw boxes on frame

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Start the video capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

# Start the frame processing thread
process_thread = threading.Thread(target=process_frames)
process_thread.start()

# Wait for the threads to finish
capture_thread.join()
process_thread.join()

# Close the display window
cv2.destroyAllWindows()
