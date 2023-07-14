from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse

def create_app(shared_data):
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
    connections = []

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):

        await websocket.accept()
        connections.append(websocket)

        while True:
            try:
                data = await websocket.receive_text()
                for connection in connections:
                    await connection.send_text(data)
                key, value = data.split(": ")
                if key == 'conf':
                    shared_data['conf'] = int(value) / 100
            except ValueError:
                print("Value Error in Try statement")
            except WebSocketDisconnect:
                connections.remove(websocket)
                break
    
    @app.get("/")
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    
    return app
