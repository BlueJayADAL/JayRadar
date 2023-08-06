from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pipelines import PipelineManager
from multiprocessing import Queue
from fastapi.responses import StreamingResponse
from networktables import NetworkTables
import cv2


class ReactUI:
    def __init__(
        self,
        manager: PipelineManager,
        q_in: Queue, ip="0.0.0.0",
        port: int = 8000,
        nt_ip="10.1.32.27",
        nt_table="JayRadar"
    ):
        """Initializes a ReactUI instance.

        Args:
            manager (PipelineManager): An instance of the PipelineManager class.
            q_in (Queue): A multiprocessing.Queue for input frames.
            ip (str, optional): The IP address to run the server on. Defaults to "0.0.0.0".
            port (int, optional): The port to run the server on. Defaults to 8000.
            nt_ip (str, optional): The IP address of the NetworkTables server. Defaults to "10.1.32.27".
            nt_table (str, optional): The name of the NetworkTable. Defaults to "JayRadar".
        """
        self.root = Path(__file__).resolve().parents[2]

        self.app = FastAPI()
        self.configure_static()

        self.ip = ip
        self.port = port
        self.manager = manager
        self.q_in = q_in
        self.nt_ip = nt_ip
        self.nt_table = nt_table
        self.connections = []

    def value_changed(self, table, key, value, isNew):
        """Callback function for networktables.ValueChangedListener.

        Args:
            table: The networktables.Table that received the change.
            key: The key of the entry that changed.
            value: The new value of the entry.
            isNew: True if the entry is new, False if it already existed.
        """
        if key == "pipeline":
            self.manager.load_from_json(f"./configs/{value}.json")

    def get_frame(self):
        """Generator function that yields frames as MJPEG response.

        Yields:
            bytes: The frame data as MJPEG response.
        """
        while True:
            frame = self.q_in.get()

            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()

                # Yield the frame data as MJPEG response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n'
                       + frame_data + b'\r\n')

    async def send_config(self, websocket):
        """Sends the current configuration to the WebSocket client.

        Args:
            websocket: The WebSocket connection.
        """
        active_pipes = self.manager.get_active_pipes()
        config = self.manager.get_configs_copy()
        for pipe in active_pipes:
            await websocket.send_text(f"{pipe}/active: {True}")
            for key, value in config[pipe].items():
                await websocket.send_text(f"{pipe}/{key}: {value}")

    async def manage_websocket_info(self, pipe, key, value):
        """Manages configuration updates received from the WebSocket client.

        Args:
            pipe: The name of the pipeline.
            key: The configuration key.
            value: The new configuration value.
        """
        if key == "active":
            if value.lower() == "false":
                self.manager.delete_pipe(pipe)
            elif value.lower() == "true":
                if pipe not in self.manager.get_active_pipes():
                    self.manager.add_pipe(pipe)
        elif key == "save":
            self.manager.save_to_json(f"./configs/{value}.json")
        elif key == "config":
            self.manager.load_from_json(f"./configs/{value}.json")
            for connection in self.connections:
                await self.send_config(connection)
        else:
            self.manager.update_configs(pipe, key, value)

    def configure_static(self):
        """Configures the static files for the FastAPI app."""
        client_build_path = self.root / "client/dist"
        self.app.mount(
            "/static", StaticFiles(directory=client_build_path), name="static")

    def configure_routes(self):
        """Configures the routes for the FastAPI app."""
        # Set up the networktables for the app
        NetworkTables.initialize(server=self.nt_ip)
        self.table = NetworkTables.getTable(self.nt_table)

        # Add a listener to be able to load manager dynamically
        self.table.addEntryListener(self.value_changed)

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            await self.send_config(websocket)

            # Add the new connection to the list
            self.connections.append(websocket)
            while True:
                try:
                    data = await websocket.receive_text()
                    pipe, key, value = data.split("/")
                    # Broadcast the received message to all connected clients
                    for connection in self.connections:
                        await connection.send_text(f"{pipe}/{key}: {value}")

                    await self.manage_websocket_info(pipe, key, value)

                except WebSocketDisconnect:
                    self.connections.remove(websocket)
                    break

        @self.app.get('/video_feed')
        def video_feed():
            # Route for streaming video feed
            return StreamingResponse(
                self.get_frame(),
                media_type='multipart/x-mixed-replace; boundary=frame')

        @self.app.get("/{full_path:path}")
        async def serve_react_app():
            # Route for serving the React app. Any routes not covered by the API will be served the React app.
            client_build_path = self.root / "client/dist/index.html"
            return FileResponse(client_build_path)

    def run(self):
        """Runs the FastAPI app and starts the server."""
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app, host=self.ip, port=self.port)
        self.release()

    def release(self):
        """Releases any resources used by the ReactUI instance."""
        self.manager.release()
