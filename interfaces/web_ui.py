from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from networktables import NetworkTables
from pipelines import PipelineManager
from multiprocessing import Queue
import os
import cv2

class WebUI:
    def __init__(self, manager:PipelineManager, q_in: Queue, ip="0.0.0.0", port:int=8000, nt_ip="10.1.32.27", nt_table="JayRadar"):
        self.app = FastAPI()
        static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        self.app.mount("/static", StaticFiles(directory=static_path), name="static")
        self.templates = Jinja2Templates(directory=templates_path)
        self.ip = ip
        self.port = port
        self.nt_ip = nt_ip
        self.nt_table = nt_table
        self.manager = manager
        self.q_in = q_in
        self.connections =[]

    def value_changed(self, table, key, value, isNew):
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()

    def get_frame(self):
        while True:
            frame = self.q_in.get()

            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                
                # Yield the frame data as MJPEG response
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
    
    def configure_routes(self):

        #Set up the networktables for the app
        NetworkTables.initialize(server=self.nt_ip)
        self.table = NetworkTables.getTable(self.nt_table)

        #Add a listener to be able to load manager dynamically
        self.table.addEntryListener(self.value_changed)

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
        
        @self.app.get('/video_feed')
        def video_feed():
            # Route for streaming video feed
            return StreamingResponse(self.get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')


    def run(self):
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app, host=self.ip, port=self.port)
        self.release()

    def release(self):
        self.manager.release()