import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open the camera")
    exit()

# Initial property values
brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
contrast = cap.get(cv2.CAP_PROP_CONTRAST)

while True:
    # Capture frame from the webcam
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Video Feed', frame)

    # Capture keyboard events
    key = cv2.waitKey(1)

    # Adjust brightness and contrast based on key presses
    if key == ord('w'):  # Increase brightness
        brightness += 1
        print(f"Brightness: {brightness}")
    elif key == ord('s'):  # Decrease brightness
        brightness -= 1
        print(f"Brightness: {brightness}")
    elif key == ord('e'):  # Increase contrast
        contrast += 1
        print(f"Contrast: {contrast}")
    elif key == ord('d'):  # Decrease contrast
        contrast -= 1
        print(f"Contrast: {contrast}")
    elif key == ord('q'):  # Quit the program
        break

    # Set the adjusted brightness and contrast values
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    cap.set(cv2.CAP_PROP_CONTRAST, contrast)

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
