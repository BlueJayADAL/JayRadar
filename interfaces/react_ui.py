from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pipelines import PipelineManager
from multiprocessing import Queue
import os


class ReactUI:

    def __init__(
        self,
        manager: PipelineManager,
        q_in: Queue, ip="0.0.0.0",
        port: int = 8000,
    ):
        self.app = FastAPI()
        static_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "react_ui/build/static"
        )
        print(static_path)

        self.app.mount(
            "/static",
            StaticFiles(directory=static_path),
            name="static"
        )

        self.ip = ip
        self.port = port
        self.manager = manager
        self.q_in = q_in

    def configure_routes(self):

        @self.app.get("/{full_path:path}")
        async def serve_react_app(full_path: str):
            return FileResponse(Path("interfaces/react_ui/build/index.html"))

    def run(self):
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app, host=self.ip, port=self.port)
        self.release()

    def release(self):
        self.manager.release()
