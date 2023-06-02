from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import socket

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("slider_test.html", {"request": request})

@app.post("/slider")
async def update_slider_value(slider_value: dict):
    value = slider_value.get("value")
    print(f"Slider value: {value}")
    return {"message": "Slider value received"}

if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname())
    import uvicorn
    uvicorn.run(app, host=ip_address, port=8000)
