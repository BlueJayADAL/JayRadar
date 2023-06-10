import cv2
from fastapi import FastAPI, Request
from PIL import Image
from io import BytesIO
from capture import frame_queue, process_event
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_frame():
    cap = cv2.VideoCapture(0)
    while True:
        # Get the latest frame from the queue
        ret, frame = cap.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
            
        # Yield the frame data as MJPEG response
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.get('/')
def index(request: Request):
    # Render the index.html template with current confidence threshold value
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    from constants import SOCKET_IP

    uvicorn.run(app, host=SOCKET_IP, port=8000)