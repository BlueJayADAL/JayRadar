import multiprocessing as mp
from camera import WebCamera
from pipelines import DeepLearning
import cv2


if __name__ == "__main__":
    # Create the multiprocessing queues
    frame_q = mp.Queue(maxsize=1)
    yolo_q = mp.Queue()

    # Create and start the camera process
    camera = WebCamera(0, frame_q)
    camera_process = mp.Process(target=camera.start_capture)
    camera_process.start()

    pipeline = DeepLearning(frame_q, yolo_q)
    pipeline_process = mp.Process(target=pipeline.start_pipeline)
    pipeline_process.start()



    while True:
        frame = yolo_q.get()
        if frame is not None:
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cv2.destroyAllWindows()
    # Terminate the processes.
    camera_process.terminate()
    pipeline_process.terminate()