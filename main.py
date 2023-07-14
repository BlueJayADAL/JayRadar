import multiprocessing as mp
from camera import WebCamera
from pipelines import DeepLearning
from web import create_app
import uvicorn


if __name__ == "__main__":
    # Create the multiprocessing queues
    frame_q = mp.Queue(maxsize=1)
    yolo_q = mp.Queue()

    manager = mp.Manager()

    pipeline_config = manager.dict()

    pipeline_config['conf'] = .25

    # Create and start the camera process
    camera = WebCamera(frame_q)
    camera_process = mp.Process(target=camera.start_capture)
    camera_process.start()

    pipeline = DeepLearning(q_in=frame_q, q_out=yolo_q, pipeline_config=pipeline_config)
    pipeline_process = mp.Process(target=pipeline.start_pipeline)
    pipeline_process.start()

    app = create_app(pipeline_config)
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # Terminate the processes.
    camera_process.terminate()
    pipeline_process.terminate()