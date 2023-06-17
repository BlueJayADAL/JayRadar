import cv2
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_frame():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n'
        )


class Slider(BaseModel):
    key: str
    value: float


class Checkbox(BaseModel):
    key: str
    value: bool


class TextBox(BaseModel):
    key: str
    value: str


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/sliders')
def sliders(slider: Slider):
    print(f"Slider: {slider.key} = {slider.value}")
    return {"message": "Slider value received"}


@app.post('/checkboxes')
def checkboxes(checkbox: Checkbox):
    print(f"Checkbox: {checkbox.key} = {checkbox.value}")
    return {"message": "Checkbox value received"}


@app.post('/textboxes')
def textboxes(textbox: TextBox):
    print(f"Textbox: {textbox.key} = {textbox.value}")
    return {"message": "Textbox value received"}


@app.get('/video_feed')
def video_feed():
    return StreamingResponse(
        get_frame(), media_type='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == "__main__":
    import uvicorn

    ip_addr = '10.1.32.27'

    uvicorn.run(app, host=ip_addr, port=8000)
