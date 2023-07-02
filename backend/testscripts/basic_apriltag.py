import cv2
import numpy as np
from pupil_apriltags import Detector
import time

# Initialize the AprilTag detector
detector = Detector(families='tag16h5')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initial property values
brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
contrast = cap.get(cv2.CAP_PROP_CONTRAST)
exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

# Define the minimum and maximum area thresholds
min_area = 1000
max_area = 409600

total_time = 0
iteration_count = 0

while True:
    start_time = time.time()
    # Capture frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the grayscale frame
    tags = detector.detect(gray, tag_size=.1524)

    # Draw a dot at the center of each reliable detected tag
    for tag in tags:
        if tag.tag_id > 0 and tag.tag_id <= 8:
            corners = np.array(tag.corners, dtype=np.int32)
            area = cv2.contourArea(corners)
            if min_area < area < max_area:
                # Convert the corner coordinates to integers
                corners = corners.reshape((-1, 1, 2))

                # Draw markers on the corners
                cv2.polylines(frame, [corners], True, (0, 255, 0), 2)
                center = (int(tag.center[0]), int(tag.center[1]))  # Convert center coordinates to integers
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                #print(tag)

    elapsed_time = time.time() - start_time

    # Accumulate the total time and increment the iteration count
    total_time += elapsed_time
    iteration_count += 1
    # Display the frame
    cv2.imshow('Frame', frame)

    # Exit the loop if 'q' is pressed
    # Capture keyboard events
    key = cv2.waitKey(1)

    # Adjust brightness and contrast based on key presses
    if key == ord('w'):  # Increase brightness
        brightness += 1
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        print(f"Brightness: {brightness}")
    elif key == ord('s'):  # Decrease brightness
        brightness -= 1
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        print(f"Brightness: {brightness}")
    elif key == ord('e'):  # Increase contrast
        contrast += 1
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        print(f"Contrast: {contrast}")
    elif key == ord('d'):  # Decrease contrast
        contrast -= 1
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        print(f"Contrast: {contrast}")
    elif key == ord('r'):  # Increase contrast
        exposure += 1
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        print(f"Expsure: {exposure}")
    elif key == ord('f'):  # Decrease contrast
        exposure -= 1
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        print(f"Expsure: {exposure}")
    elif key == ord('q'):  # Quit the program
        break

# Calculate the average time per iteration
average_time = total_time / iteration_count

# Print the average time
print(f"Average Time per Iteration: {average_time} seconds")
print(f"Frames per Second: {1/average_time}")

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
