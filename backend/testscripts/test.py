import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
#video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model.predict(frame)
        for result in results:
            boxes = result.boxes # get boxes on cpu in numpy
            for box in boxes: # iterate boxes
                x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
                print(f"Cordinates: ({x1},{y1}) + ({x2},{y2})") # print boxes
                #cv2.rectangle(frame, r[:2], r[2:], (0,255,0), 2) # draw boxes on frame

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
