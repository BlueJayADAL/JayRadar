import threading
from collections import deque
from camera import WebCamera
from pipelines import DeepLearning
from web import create_app
import uvicorn
import cv2


if __name__ == "__main__":
    # Create the multithreading dequeues
    frame_q = deque(maxlen=5)
    yolo_q = deque(maxlen=5)

    pipeline_config = {
        "conf": .25,
    }

    # Create and start the camera process
    camera = WebCamera(frame_q)
    
    pipeline = DeepLearning(
        q_in = frame_q,
        q_out = yolo_q,
        pipeline_config = pipeline_config
        )
    

    
    camera_process = threading.Thread(target=camera.start_capture)
    pipeline_process = threading.Thread(target=pipeline.start_pipeline)
    
    camera_process.start()
    pipeline_process.start()

    #app = create_app(pipeline_config)
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    while True:
        pass
    #cv2.destroyAllWindows()
    # Terminate the processes.
    #camera_process.join()
    #pipeline_process.join()