import cv2
import json
import threading
from ultralytics import YOLO
from constants import MODEL_NAME, NT_SERVER_IP, TABLE_NAME, CONFIG_TYPES
from capture import frame_queue
from networktables import NetworkTables
import time

network_setup_event = threading.Event()

NetworkTables.initialize(NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

# Lock for accessing NetworkTables vairables. 
# This ensures that no other threads have access when this thread is trying to access them
nt_lock = threading.Lock()

config_event = threading.Event()

def save_config(filename, config):
    filename = f'./configs/{filename}.json'
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)

def load_config(filename, config):
    filename = f'./configs/{filename}.json'
    try:    
        with open(filename, 'r') as file:
            new_config = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return config
    typecasted_config = {}
    for key, value in new_config.items():
        if key == "class":
            try:
                typecasted_value = [int(v) for v in value]
                typecasted_config[key] = typecasted_value
            except (ValueError, TypeError):
                # Failed to typecast, use original value
                typecasted_config[key] = config[key]
        else:
            try:
                typecasted_value = CONFIG_TYPES[key](value)
                typecasted_config[key] = typecasted_value
            except (ValueError, TypeError):
                # Failed to typecast, use original value
                typecasted_config[key] = config[key]
    
        #nt.putValue(key, config[key])


    return typecasted_config
config = {  
        "conf": 25,
        "iou": 70,
        "half": False,
        "ss": False,
        "ssd": False,
        "max": 5,
        "img": 480,
        "class": [
            -1
        ]
    }
config = load_config('default', config)

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
    
    def value_changed(table, key, value, isNew):
        global config
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()
        with nt_lock:
            print("Network_Thread acquired lock")
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
            print("Network_Thread released lock")
    
    time.sleep(1)
    nt.addEntryListener(value_changed)

    while True:
        #time.sleep(2)
        if frame_queue:
            frame = frame_queue[-1]  # Get the newest frame from the deque

            with nt_lock:
                print("Process_Thread acquired lock")
                conf = config['conf'] / 100
                iou = config['iou'] / 100
                half = config['half']
                save = config['ss']
                save_conf = config['ssd']
                max_det = config['max']
                image_size = config['img']
                classes = config['class']
                print("Process_Thread released lock")
            # If the first index of classes is -1
            print(f'Max_det: {max_det}')
            print(f'conf: {conf}')
            if (classes[0]==-1):
                # Process the frame using YOLOv8 without class filter
                results = model.predict(
                    frame.copy(),
                    conf=conf,
                    iou=iou,
                    #half=half,
                    #device=device,
                    save=save,
                    save_conf=save_conf,
                    max_det=max_det,
                    imgsz = image_size
                    )
            else:
            # Otherwise, process the frame using YOLOv8 with class filter
                results = model.predict(
                    frame.copy(),
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
            result = results[0]  # Get the detection results from the first image in the batch
            
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
            
            # Annotate and display the frame for testing, will be removed in final version
            annotated_frame = results[0].plot()

            
            cv2.imshow('YOLOv8 Inference', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break