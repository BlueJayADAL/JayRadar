import cv2
import numpy as np
from PIL import Image, ImageDraw
#from ultralytics import YOLO
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from backend import draw_bounding_boxes, detect_objects_on_image

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Set initial confidence threshold value
confidence_threshold = 50

def generate():
    # Generator function to process video frames and stream as MJPEG
    
    # Open video capture device
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        
        # Convert frame to PIL Image
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Perform object detection on the frame
        results = detect_objects_on_image(frame_pil, confidence_threshold)
        
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

@app.get('/')
def index(request: Request):
    # Render the index.html template with current confidence threshold value
    return templates.TemplateResponse("fastapi.html", {"request": request, "confidence": confidence_threshold})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.post('/update_threshold')
async def update_threshold(confidence: dict):
    # Update the confidence threshold based on the slider value
    global confidence_threshold
    confidence_threshold = int(confidence.get("value"))
    return 'OK'

if __name__ == "__main__":
    import uvicorn
    import socket
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    uvicorn.run(app, host=ip_address, port=8000)
