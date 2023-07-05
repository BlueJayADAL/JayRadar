import threading
from collections import deque
from ultralytics import YOLO
from constants import MODEL_NAME, MAX_FRAMES
from capture import frame_queue
import time

nn_queue = deque(maxlen=MAX_FRAMES)

nn_event = threading.Event()

nn_lock = threading.Lock()

nn_config = {  
    "conf": 25,
    "iou": 70,
    "half": False,
    "ss": False,
    "ssd": False,
    "max": 7,
    "img": 640,
    "class": [
        -1
    ]
}

nn_updated = False

def average_last_iterations(times, iterations):
    return sum(times[-iterations:]) / iterations

def process_frames():
    global nn_config, nn_updated
    model = YOLO(MODEL_NAME)

    conf = nn_config['conf'] / 100
    iou = nn_config['iou'] / 100
    half = nn_config['half']
    save = nn_config['ss']
    save_conf = nn_config['ssd']
    max_det = nn_config['max']
    image_size = nn_config['img']
    classes = nn_config['class']

    times = []
    max_iterations = 50  # Adjust this value to set the maximum size of the 'times' list
    iterations = 0  

    while True:
        start_time = time.time()
        if frame_queue:
            frame = frame_queue[-1]

            conf = nn_config['conf'] / 100
            iou = nn_config['iou'] / 100
            half = nn_config['half']
            save = nn_config['ss']
            save_conf = nn_config['ssd']
            max_det = nn_config['max']
            image_size = nn_config['img']
            classes = nn_config['class']
            if (classes[0]==-1):
                classes = None
            results = model.predict(
                frame,
                conf=conf,
                iou=iou,
                half=half,
                save=save,
                save_txt=save_conf,
                max_det=max_det,
                classes=classes,
                imgsz = image_size,
                verbose=False
            )
         
            annotated_frame = results[0].plot()

            nn_queue.append(annotated_frame) 

            nn_event.set()

            end_time = time.time()
            iteration_time = end_time - start_time
            times.append(iteration_time)

            if iterations< max_iterations:
                iterations +=1

            if len(times) > max_iterations:
                times = times[-max_iterations:]

            avg_last_x_iterations = average_last_iterations(times, iterations)
            print(f"Time: {iteration_time:.4f}s | "
                f"Avg Last {iterations} Iterations: {avg_last_x_iterations:.4f}s")