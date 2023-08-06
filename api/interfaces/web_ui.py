from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pipelines import PipelineManager
from multiprocessing import Queue
import os


class WebUI:
    """
    WebUI class for providing a web-based user interface to interact with a video processing pipeline.

    This class utilizes FastAPI to create a web server that serves a live video feed from the video processing pipeline.
    The user can interact with the pipeline by accessing the web interface, updating pipe configurations, and
    monitoring real-time results.

    Args:
        manager (PipelineManager): The PipelineManager object used to manage the video processing pipeline.
        q_in (Queue): The multiprocessing Queue to receive frames from the video processing pipeline.
        ip (str, optional): The IP address for the FastAPI server. Defaults to localhost: "0.0.0.0".
        port (int, optional): The port number for the FastAPI server. Defaults to 8000.
        nt_ip (str, optional): The IP address of the NetworkTables server. Defaults to "10.1.32.27".
        nt_table (str, optional): The NetworkTables table name. Defaults to "JayRadar".
    """  # noqa: E501

    def __init__(
        self,
        manager: PipelineManager,
        q_in: Queue, ip="0.0.0.0",
        port: int = 8000,
        nt_ip="10.1.32.27",
        nt_table="JayRadar"
    ):
        self.app = FastAPI()
        static_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "static")
        templates_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "templates")
        self.app.mount(
            "/static", StaticFiles(directory=static_path), name="static")
        self.templates = Jinja2Templates(directory=templates_path)
        self.ip = ip
        self.port = port
        self.nt_ip = nt_ip
        self.nt_table = nt_table
        self.manager = manager
        self.q_in = q_in
        self.connections = []

    def configure_routes(self):

        @self.app.get("/")
        async def home(request: Request):
            return self.templates.TemplateResponse(
                "index.html",
                {"request": request}
            )

    def run(self):
        """
        Run the web-based user interface.

        The method starts the FastAPI server and configures the necessary routes for the web interface. The user can
        interact with the video processing pipeline through the web interface by accessing the root page to view the
        live video feed and using the WebSocket connection to update pipe configurations and monitor real-time results.
        """  # noqa: E501
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app, host=self.ip, port=self.port)
        self.release()

    def release(self):
        """
        Release resources and terminate the pipeline manager.

        The method releases the resources used by the pipeline manager and terminates the associated pipeline process.
        """  # noqa: E501
        self.manager.release()
