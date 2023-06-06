import cv2
import numpy as np
from PIL import Image, ImageDraw
from flask import Flask, Response, render_template, request
from backend import draw_bounding_boxes, detect_objects_on_image

app = Flask(__name__)

confidence_threshold = 50

def generate():
    # Check if a CSI camera is available
    csi_camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if csi_camera.isOpened():
        video_source = csi_camera
    else:
        video_source = cv2.VideoCapture(0)

    while True:
        # Read the frame from the video source
        ret, frame = video_source.read()

        # Convert the frame to PIL Image format
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform object detection on the frame
        results = detect_objects_on_image(frame_pil, confidence_threshold)

        # Draw bounding boxes on the frame
        frame_pil_with_boxes = draw_bounding_boxes(frame_pil.copy(), results)

        # Convert the frame back to OpenCV format for streaming
        frame_with_boxes = cv2.cvtColor(np.array(frame_pil_with_boxes), cv2.COLOR_RGB2BGR)

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame_with_boxes)

        # Yield the encoded frame as a byte string
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    # Update the confidence threshold based on the slider value
    global confidence_threshold
    confidence_threshold = int(request.form['confidence'])
    return 'OK'

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
