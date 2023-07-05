import cv2
import json
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from capture import frame_queue, process_event
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from constants import NT_SERVER_IP, TABLE_NAME
from detection import nn_lock, nn_config, nn_updated, nn_queue, nn_event
from networktables import NetworkTables

complete_config = {  
    "cam": 0,
    "auto_exp": False,
    "exp": -5,
    "bri": 0,
    "cont": 1.0,
    "red": 0,
    "gre": 0,
    "blu": 0,
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

nn_keys = {  
        "conf": int,
        "iou": int,
        "half": bool,
        "ss": bool,
        "ssd": bool,
        "max": int,
        "class": list
    }

NetworkTables.initialize(NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

# Maintain a list of active connections
connections = []

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def update_config(key, value):
    global complete_config, nn_keys, nn_lock, nn_config, nn_updated
    if key == "config":
        load_config(value)
    if key == "save_config":
        save_config(value)
    if key in nn_keys:
        nn_updated = True
        with nn_lock:
            if key == "class":
                try:
                    typecasted_value = [int(v) for v in value]
                    nn_config[key] = typecasted_value
                    complete_config[key] = typecasted_value
                    print(f"nn_config[{key}] = {nn_config[key]}")
                except (ValueError, TypeError):
                    pass
            else:
                try:
                    typecasted_value = nn_keys[key](value)
                    nn_config[key] = typecasted_value
                    complete_config[key] = typecasted_value
                    print(f"nn_config[{key}] = {nn_config[key]}")
                except (ValueError, TypeError):
                    # Failed to typecast, use original value
                    pass

def save_config(filename):
    global complete_config
    filename = f'./configs/{filename}.json'
    with open(filename, 'w') as file:
        json.dump(complete_config, file, indent=4)

def load_config(filename):
    filename = f'./configs/{filename}.json'
    try:    
        with open(filename, 'r') as file:
            print(f'Sucessfully loaded {filename}')
            new_config = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return -1
    

    for key, value in new_config.items():
        update_config(key, value)
    return 0

def value_changed(table, key, value, isNew):
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()
        update_config(key, value)
            
nt.addEntryListener(value_changed)

def draw_bounding_box(frame, x, y, w, h):
    x1, y1 = int(x - w/2), int(y - h/2)  # Calculate top-left corner coordinates
    x2, y2 = int(x + w/2), int(y + h/2)  # Calculate bottom-right corner coordinates

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw the bounding box

    return frame

def draw_crosshair(frame, x, y):
    cv2.drawMarker(frame, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
    return frame

def get_frame():
    while True:
        # Get the latest frame from the queue
        process_event.wait()  # Wait for the event to be set, so we know there's a frame
        process_event.clear()  # Clear the event, it will be set again next time
        if nn_queue:
            frame = frame_queue[-1].copy()

            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                
                # Yield the frame data as MJPEG response
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

def get_nn_frame():
    while True:
        # Get the latest frame from the queue
        nn_event.wait()  # Wait for the event to be set, so we know there's a frame
        nn_event.clear()  # Clear the event, it will be set again next time
        if nn_queue:
            frame = nn_queue[-1].copy()

            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                
                # Yield the frame data as MJPEG response
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global nn_config
    await websocket.accept()
    # Add the new connection to the list
    connections.append(websocket)

    with nn_lock:
        for key, value in complete_config.items():
            data = f'{key}: {value}'
            await websocket.send_text(data)


    while True:
        try:
            data = await websocket.receive_text()
            print()
            print('UPDATE FROM WEB GUI FOUND')
            print(f"DATA: {data}")
            print()
            for connection in connections:
                await connection.send_text(data)
            key, value = data.split(": ")
            update_config(key, value)
            if key == 'config':
                for key, value in complete_config.items():
                    data = f'{key}: {value}'
                    for connection in connections:
                        await connection.send_text(data)


        except ValueError:
            print("Value Error in Try statement")
        except WebSocketDisconnect:
            connections.remove(websocket)
            break


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/nn_feed')
def nn_feed():
    # Route for streaming video feed
    return StreamingResponse(get_nn_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("standard.png")

if __name__ == "__main__":
    import uvicorn
    import threading
    from capture import capture_frames

    capture_thread = threading.Thread(target = capture_frames)
    capture_thread.start()

    uvicorn.run(app, host='0.0.0.0', port=8000)