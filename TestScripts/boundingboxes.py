import cv2
import numpy as np
from PIL import Image, ImageDraw
from ultralytics import YOLO

def draw_bounding_boxes(image, boxes):
    """
    Function to draw bounding boxes on an image.
    :param image: PIL Image object
    :param boxes: List of bounding boxes in format [[x1, y1, x2, y2, object_type, probability], ...]
    :return: Image with bounding boxes drawn
    """
    draw = ImageDraw.Draw(image)  # Create an ImageDraw object to draw on the image
    for box in boxes:  # Iterate over each bounding box in the list
        x1, y1, x2, y2, _, confidence = box  # Unpack the bounding box coordinates (ignoring object type and probability)
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=2)  # Draw a rectangle on the image using the coordinates, color, and width
        object_type = box[4]  # Get the object type from the bounding box list
        center_x = (x1 + x2) // 2  # Calculate the x-coordinate of the bounding box center
        center_y = (y1 + y2) // 2  # Calculate the y-coordinate of the bounding box center
        draw.text((center_x, y1 - 10), f"{object_type}", fill="red")
        draw.text((center_x, y1 - 30), f"Confidence: {confidence}", fill="red")  # Add text label for center coordinates above the bounding box
    return image  # Return the modified image with bounding boxes drawn

def detect_objects_on_image(buf):
    """
    Function receives an image,
    passes it through YOLOv8 neural network
    and returns an array of detected objects
    and their bounding boxes
    :param buf: Input image file stream
    :return: Array of bounding boxes in format 
    [[x1,y1,x2,y2,object_type,probability],..]
    """
    model = YOLO("yolov8n.pt")  # Create an instance of the YOLOv8 model
    results = model.predict(buf, conf=50/100)  # Perform object detection on the image
    result = results[0]  # Get the detection results from the first image in the batch
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]  # Extract the bounding box coordinates and round them
        class_id = box.cls[0].item()  # Get the class ID of the detected object
        prob = round(box.conf[0].item(), 2)  # Get the detection probability
        output.append([
            x1, y1, x2, y2, result.names[class_id], prob
        ])  # Append the bounding box information to the output list
    return output

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to PIL Image format
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Perform object detection on the frame
    results = detect_objects_on_image(frame_pil)

    # Draw bounding boxes on the frame
    frame_pil_with_boxes = draw_bounding_boxes(frame_pil.copy(), results)

    # Convert the frame back to OpenCV format for display
    frame_with_boxes = cv2.cvtColor(np.array(frame_pil_with_boxes), cv2.COLOR_RGB2BGR)

    # Print the results
    for box in results:
        x1, y1, x2, y2, object_type, probability = box
        x_center = (x1 + x2) / 2  # Calculate the x-coordinate of the bounding box center
        y_center = (y1 + y2) / 2  # Calculate the y-coordinate of the bounding box center
        print("Object Type:", object_type)
        print("Center coordinates: (x={}, y={})".format(x_center, y_center))
        print()

    # Display the frame with bounding boxes
    cv2.imshow("Object Detection", frame_with_boxes)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and close any open windows
cap.release()
cv2.destroyAllWindows()
