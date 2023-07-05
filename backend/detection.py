import threading
from collections import deque
from ultralytics import YOLO
from constants import MODEL_NAME, MAX_FRAMES
from capture import frame_queue

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
    while True:
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

            print(f'Confidence = {conf}')
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
                verbose=True
            )
         
            annotated_frame = results[0].plot()

            nn_queue.append(annotated_frame) 

            nn_event.set()