import cv2
import json
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, UploadFile, File
from capture import frame_queue, process_event
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from detection import nn_lock, nn_config, nn_queue, nn_event
from send import filtered_queue, nt
import os

complete_config = {  
    "cam": 0,
    "auto_exp": False,
    "exp": -5,
    "bri": 0,
    "cont": 1.0,
    "red": 0,
    "gre": 0,
    "blu": 0,
    "model": "./models/yolov8n.pt",
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
    "model": str,        
    "conf": int,
    "iou": int,
    "half": bool,
    "ss": bool,
    "ssd": bool,
    "max": int,
    "class": list
    }

# Maintain a list of active connections
connections = []

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
folder_path = './models'

def list_files():
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_list.append(file_path)
    return file_list

def update_config(key, value):
    global complete_config, nn_keys, nn_lock, nn_config
    if key == "config":
        load_config(value)
    if key == "save_config":
        save_config(value)
    if key in nn_keys:
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

def draw_bounding_box(frame, x, y, w, h):
    x1, y1 = int(x - w/2), int(y - h/2)  # Calculate top-left corner coordinates
    x2, y2 = int(x + w/2), int(y + h/2)  # Calculate bottom-right corner coordinates

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw the bounding box

    return frame

def draw_crosshair(frame, x, y):
    cv2.drawMarker(frame, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
    return frame

def value_changed(table, key, value, isNew):
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()
        update_config(key, value)
            
nt.addEntryListener(value_changed)

def get_frame():
    while True:
        # Get the latest frame from the queue
        process_event.wait()  # Wait for the event to be set, so we know there's a frame
        process_event.clear()  # Clear the event, it will be set again next time
        if frame_queue:
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
                

def get_filtered_frame():
    while True:
        # Get the latest frame from the queue
        process_event.wait()  # Wait for the event to be set, so we know there's a frame
        process_event.clear()  # Clear the event, it will be set again next time
        if frame_queue and filtered_queue:
            frame = frame_queue[-1].copy()
            result = filtered_queue[-1]

            if frame is not None:

                crosshair_frame = draw_crosshair(frame, 320, 240)

                if result is not None:
                    final_frame = draw_bounding_box(crosshair_frame, result[0], result[1], result[2], result[3])
                else:
                    final_frame = crosshair_frame

                ret, buffer = cv2.imencode('.jpg', final_frame)
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
    files = list_files()
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/nn_feed')
def nn_feed():
    # Route for streaming video feed
    return StreamingResponse(get_nn_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/filtered_feed')
def filtered_feed():
    # Route for streaming video feed
    return StreamingResponse(get_filtered_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("standard.png")

@app.post("/upload")
async def upload_file(request: Request, upload_file: UploadFile = File(...)):
    if upload_file.filename:
        filename = upload_file.filename
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "wb") as f:
            f.write(await upload_file.read())
    files = list_files()
    return templates.TemplateResponse("index.html", {"request": request, "files": files})
   

if __name__ == "__main__":
    import uvicorn
    import threading
    from capture import capture_frames

    capture_thread = threading.Thread(target = capture_frames)
    capture_thread.start()

    uvicorn.run(app, host='0.0.0.0', port=8000)