from fastapi import FastAPI

class WebUI:
    def __init__(self):
        self.app = FastAPI()

    def configure_routes(self):
        @self.app.get("/")
        def root():
            return {"message": "Hello, World!"}

    def run(self):
        self.configure_routes()
        import uvicorn
        uvicorn.run(self.app)