import cv2

stream_url = "http://localhost:8000/video_feed"

# Open the MJPEG stream
stream = cv2.VideoCapture(stream_url)

while True:
    # Read frame from the stream
    ret, frame = stream.read()

    if not ret:
        break

    # Display the frame in a cv2 window
    cv2.imshow("MJPEG Stream", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
stream.release()
cv2.destroyAllWindows()
