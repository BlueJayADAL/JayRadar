import multiprocessing as mp
from camera import WebCamera
from pipelines import DeepLearning
import cv2


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



    while True:
        frame = yolo_q.get()
        if frame is not None:
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('1'):
                pipeline_config['conf'] = 1
            elif key == ord('0'):
                pipeline_config['conf'] = 0


    cv2.destroyAllWindows()
    # Terminate the processes.
    camera_process.terminate()
    pipeline_process.terminate()