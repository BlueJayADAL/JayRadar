import cv2
from fastapi import FastAPI, Request
from PIL import Image
from io import BytesIO
from capture import frame_queue, process_event
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from constants import HTML_PAGE

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_frame():
        
    while True:
        # Get the latest frame from the queue
        process_event.wait()  # Wait for the event to be set, so we know there's a frame
        process_event.clear()  # Clear the event, it will be set again next time

        frame = frame_queue[-1] if frame_queue else None

        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            
            # Yield the frame data as MJPEG response
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.get('/')
def index(request: Request):
    # Render the index.html template with current confidence threshold value
    return templates.TemplateResponse(HTML_PAGE, {"request": request})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

