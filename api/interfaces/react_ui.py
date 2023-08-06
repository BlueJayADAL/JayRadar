from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pipelines import PipelineManager
from multiprocessing import Queue


class ReactUI:
    def __init__(
        self,
        manager: PipelineManager,
        q_in: Queue, ip="0.0.0.0",
        port: int = 8000,
    ):
        self.root = Path(__file__).resolve().parents[2]

        self.app = FastAPI()
        self.configure_static()

        self.ip = ip
        self.port = port
        self.manager = manager
        self.q_in = q_in

    def configure_static(self):
        client_build_path = self.root / "client/dist"
        self.app.mount(
            "/static", StaticFiles(directory=client_build_path), name="static")

    def configure_routes(self):
        @self.app.get("/test")
        async def test():
            return {"test": "test"}

        @self.app.get("/{full_path:path}")
        async def serve_react_app():
            client_build_path = self.root / "client/dist/index.html"
            return FileResponse(client_build_path)

    def run(self):
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app, host=self.ip, port=self.port)
        self.release()

    def release(self):
        self.manager.release()
