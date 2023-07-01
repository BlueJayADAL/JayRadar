import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open the camera")
    exit()

# Check support for camera properties
for prop_id in range(0, 100):
    value = cap.get(prop_id)
    if value != -1:
        print(f"Property ID: {prop_id}, Value: {value}")

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
