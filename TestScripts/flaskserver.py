import cv2
import numpy as np
from PIL import Image, ImageDraw
from ultralytics import YOLO
from flask import Flask, render_template, Response, request

# Initialize Flask app
app = Flask(__name__)

# Set initial confidence threshold value
confidence_threshold = 50

def get_camera():
    # Check if a CSI camera is available
    csi_camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if csi_camera.isOpened():
        return csi_camera

    # If CSI camera is not available, use the webcam
    webcam = cv2.VideoCapture(0)
    return webcam

def draw_bounding_boxes(image, boxes):
    # Function to draw bounding boxes on an image.
    draw = ImageDraw.Draw(image)
    for box in boxes:
        x1, y1, x2, y2, _, confidence = box
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=2)
        object_type = box[4]
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        draw.text((center_x, y1 - 10), f"{object_type}", fill="red")
        draw.text((center_x, y1 - 30), f"Confidence: {confidence}", fill="red")
    return image

def detect_objects_on_image(buf):
    # Function receives an image, passes it through YOLOv8 neural network,
    # and returns an array of detected objects and their bounding boxes
    
    # Initialize YOLOv8 model
    model = YOLO("yolov8n.pt")
    
    # Print the current value of the confidence threshold
    print(f"Slider Value: {confidence_threshold}")
    
    # Perform object detection on the image using YOLOv8
    results = model.predict(buf, conf=confidence_threshold / 100)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        if prob >= confidence_threshold / 100:
            output.append([
                x1, y1, x2, y2, result.names[class_id], prob
            ])
    return output

def generate():
    # Generator function to process video frames and stream as MJPEG
    
    # Open video capture device
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        
        # Convert frame to PIL Image
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Perform object detection on the frame
        results = detect_objects_on_image(frame_pil)
        
        # Draw bounding boxes on the frame
        frame_pil_with_boxes = draw_bounding_boxes(frame_pil.copy(), results)
        
        # Convert the frame back to OpenCV format
        frame_with_boxes = cv2.cvtColor(np.array(frame_pil_with_boxes), cv2.COLOR_RGB2BGR)
        
        # Print object information
        for box in results:
            x1, y1, x2, y2, object_type, probability = box
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            print("Object Type:", object_type)
            print("Center coordinates: (x={}, y={})".format(x_center, y_center))
            print("Confidence:", probability)
            print()
        
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_with_boxes)
        frame_data = buffer.tobytes()
        
        # Yield the frame data as MJPEG response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.route('/')
def index():
    # Render the index.html template with current confidence threshold value
    return render_template('index.html', confidence=confidence_threshold)

@app.route('/video_feed')
def video_feed():
    # Route for streaming video feed
    camera = get_camera()
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    # Update the confidence threshold based on the slider value
    global confidence_threshold
    confidence_threshold = int(request.form['confidence'])
    return 'OK'

if __name__ == '__main__':
    # Get the local machine's IP address
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    # Start the web server on the local machine's IP address
    app.run(host=ip_address, port=8000, debug=True)
