import cv2
import json
import threading
from collections import deque
from ultralytics import YOLO
from constants import MODEL_NAME, NT_SERVER_IP, TABLE_NAME, CONFIG_TYPES, MAX_FRAMES
from capture import frame_queue
from networktables import NetworkTables
from filters import filter_edge_crosshair
import time

debugging_queue = deque(maxlen=MAX_FRAMES)

debugging_event = threading.Event()

network_setup_event = threading.Event()

NetworkTables.initialize(NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

# Lock for accessing NetworkTables vairables. 
# This ensures that no other threads have access when this thread is trying to access them
nt_lock = threading.Lock()

config_event = threading.Event()

config = {  
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

def save_config(filename):
    global config
    filename = f'./configs/{filename}.json'
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)

def load_config(filename):
    global config
    filename = f'./configs/{filename}.json'
    try:    
        with open(filename, 'r') as file:
            print(f'Sucessfully loaded {filename}')
            new_config = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return -1
    for key, value in new_config.items():
        if key == "class":
            try:
                typecasted_value = [int(v) for v in value]
                config[key] = typecasted_value
                print(f'config[{key}] = {config[key]}')
            except (ValueError, TypeError):
                # Failed to typecast, use original value
                pass
        else:
            try:
                typecasted_value = CONFIG_TYPES[key](value)
                config[key] = typecasted_value
                print(f'config[{key}] = {config[key]}')
            except (ValueError, TypeError):
                # Failed to typecast, use original value
                pass
    return 0

def test_process():
    global config
    """
    Function to process frames from the frame queue using YOLOv8.
    """
    # Load the YOLOv8 model
    model = YOLO(MODEL_NAME)

    NetworkTables.initialize(NT_SERVER_IP)

    # Retrieve the JayRadar table for us to use
    nt = NetworkTables.getTable(TABLE_NAME)
    with nt_lock:
        load_config('default')
    
    def value_changed(table, key, value, isNew):
        global config
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()
        with nt_lock:
            print("Processing_Thread acquired lock")
            if key == "load_config":
                config = load_config(value, config)
            if key == "save_config":
                save_config(value, config)
            if key in CONFIG_TYPES:
                if key == "class":
                    try:
                        typecasted_value = [int(v) for v in value]
                        config[key] = typecasted_value
                        print()
                        print('CLASSES UPDATED')
                        print()
                        config_event.set()
                    except (ValueError, TypeError):
                        # Failed to typecast, use original value
                        print()
                        print('ERROR: TYPECASTING FAILED')
                        print()
                        pass
                else:
                    try:
                        typecasted_value = CONFIG_TYPES[key](value)
                        config[key] = typecasted_value
                        print()
                        print(f'CONFIG UPDATED: config[{key}] = {typecasted_value}')
                        print()
                        config_event.set()
                    except (ValueError, TypeError):
                        # Failed to typecast, use original value
                        print()
                        print('ERROR: TYPECASTING FAILED')
                        print()
                        pass
            print("Processing_Thread released lock")
    
    time.sleep(1)
    nt.addEntryListener(value_changed)

    while True:
        #time.sleep(2)
        if frame_queue:
            frame = frame_queue[-1]  # Get the newest frame from the deque

            with nt_lock:
                conf = config['conf'] / 100
                iou = config['iou'] / 100
                half = config['half']
                save = config['ss']
                save_conf = config['ssd']
                max_det = config['max']
                image_size = config['img']
                classes = config['class']
            # If the first index of classes is -1
            if (classes[0]==-1):
                classes = None
            results = model.predict(
                frame,
                conf=conf,
                iou=iou,
                #half=half,
                #device=device,
                save=save,
                save_conf=save_conf,
                max_det=max_det,
                classes=classes,
                imgsz = image_size
            )
            box, success_filter = filter_edge_crosshair(results[0], 320, 240)

            if success_filter:
                cx, cy, w, h = [round(x) for x in box.xywh[0].tolist()]
                a = w*h / (image_size * image_size * 3/4)
                nt.putBoolean('te', True)
                nt.putNumber('tx', cx)
                nt.putNumber('ty', cy)
                nt.putNumber('tw', w)
                nt.putNumber('th', h)
                nt.putNumber('ta', a)
            else:
                nt.putBoolean('te', False)
                nt.putNumber('tx', -1)
            """
            objects = []
            
            for index, box in enumerate(result.boxes):
                name = 'object'+str(index)
                cx, cy, w, h = [
                    x for x in box.xywh[0].tolist()
                ]  # Extract the bounding box coordinates and round them
                class_id = box.cls[0].item()  # Get the class ID of the detected object
                prob = round(box.conf[0].item(), 2)  # Get the detection probability
                output = [cx, cy, w, h, prob]  # Append the bounding box information to the output list
                objects.append(float(class_id))
                nt.putNumberArray(name, output)
            nt.putNumberArray('objects_key', objects)
            """           
            # Annotate and display the frame for testing, will be removed in final version
            annotated_frame = results[0].plot()

            debugging_queue.append(annotated_frame) 

            debugging_event.set()