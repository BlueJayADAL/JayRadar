from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

class WebUI:
    def __init__(self, ip="0.0.0.0", port:int=8000):
        self.app = FastAPI()
        static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        self.app.mount("/static", StaticFiles(directory=static_path), name="static")
        self.templates = Jinja2Templates(directory=templates_path)
        self.ip = ip
        self.port = port
        self.connections = []

    def configure_routes(self):
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            # Add the new connection to the list
            self.connections.append(websocket)
            while True:
                try:
                    data = await websocket.receive_text()
                    print(f"Server received: {data}")
                    # Broadcast the received message to all connected clients
                    for connection in self.connections:
                        await connection.send_text(data)
                except WebSocketDisconnect:
                    self.connections.remove(websocket)
                    break
                
        @self.app.get("/")
        async def home(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

    def run(self):
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app, host=self.ip, port=self.port)