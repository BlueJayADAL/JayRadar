from networktables import NetworkTables
import json
import threading
import uvicorn
import time
import cv2
from fastapi import FastAPI, Request
from capture import frame_queue, process_event
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from constants import SOCKET_IP, NT_SERVER_IP, CONFIG_TYPES, TABLE_NAME, HTML_PAGE

network_setup_event = threading.Event()

NetworkTables.initialize(NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

# Lock for accessing NetworkTables vairables. 
# This ensures that no other threads have access when this thread is trying to access them
nt_lock = threading.Lock()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def save_config(filename, config):
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)

def load_config(filename, config):
    try:    
        with open(filename, 'r') as file:
            new_config = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return config
    typecasted_config = {}
    for key, value in CONFIG_TYPES.items():
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
config = load_config('default.json', config)

def get_frame():
        
    while True:
        # Get the latest frame from the queue
        process_event.wait()  # Wait for the event to be set, so we know there's a frame
        process_event.clear()  # Clear the event, it will be set again next time

        frame = frame_queue[-1] if frame_queue else None

        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            
            # Yield the frame data as MJPEG response
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.get('/')
def index(request: Request):
    # Render the index.html template with current confidence threshold value
    return templates.TemplateResponse(HTML_PAGE, {"request": request})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')
   

def frontend():
    global config
    def value_changed(table, key, value, isNew):
        global config
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()
        with nt_lock:
            print("Network_Thread acquired lock")
            if key in CONFIG_TYPES:
                if key == "class":
                    try:
                        typecasted_value = [int(v) for v in value]
                        config[key] = typecasted_value
                        print()
                        print('CLASSES UPDATED')
                        print()
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
                    except (ValueError, TypeError):
                        # Failed to typecast, use original value
                        print()
                        print('ERROR: TYPECASTING FAILED')
                        print()
                        pass
            print("Network_Thread released lock")
    
    time.sleep(1)
    nt.addEntryListener(value_changed)
    network_setup_event.set()

    
    uvicorn.run(app, host=SOCKET_IP, port=8000)

