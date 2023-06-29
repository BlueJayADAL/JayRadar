import cv2
from fastapi import FastAPI, Request, WebSocket
from capture import frame_queue, process_event
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from constants import CONFIG_TYPES, NT_SERVER_IP, TABLE_NAME
from complete_process import nt_lock, config, debugging_queue, debugging_event, load_config, save_config
from networktables import NetworkTables

NetworkTables.initialize(NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

debugging = False

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def draw_bounding_box(frame, x, y, w, h):
    x1, y1 = int(x - w/2), int(y - h/2)  # Calculate top-left corner coordinates
    x2, y2 = int(x + w/2), int(y + h/2)  # Calculate bottom-right corner coordinates

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw the bounding box

    return frame

def draw_crosshair(frame, x, y):
    cv2.drawMarker(frame, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
    return frame

def get_frame():
    global debugging
        
    while True:
        # Get the latest frame from the queue
        if debugging:
            debugging_event.wait()
            debugging_event.clear()
            
            frame = debugging_queue[-1] if debugging_queue else None

            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                
                # Yield the frame data as MJPEG response
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        else:
            process_event.wait()  # Wait for the event to be set, so we know there's a frame
            process_event.clear()  # Clear the event, it will be set again next time

            frame = frame_queue[-1].copy() if frame_queue else None

            if frame is not None:
                te = nt.getBoolean('te', False)
                nt.putBoolean('te', te)
                if te:
                    tx = nt.getNumber('tx', -1)

                    ty = nt.getNumber('ty', -1)

                    tw = nt.getNumber('tw', -1)

                    th = nt.getNumber('th', -1)

                    frame_box = draw_bounding_box(frame, tx, ty, tw, th)
                else:
                    frame_box = frame
                frame_final = draw_crosshair(frame_box, 320, 240)
                ret, buffer = cv2.imencode('.jpg', frame_box)
                frame_data = buffer.tobytes()
                
                # Yield the frame data as MJPEG response
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


# Maintain a list of active connections
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global config, debugging
    await websocket.accept()
    # Add the new connection to the list
    connections.append(websocket)

    with nt_lock:
        for key, value in config.items():
            data = f'{key}: {value}'
            await websocket.send_text(data)


    try:
        while True:
            data = await websocket.receive_text()
            print()
            print('UPDATE FROM WEB GUI FOUND')
            print(f"DATA: {data}")
            print()
            key, value = data.split(": ")
            
            with nt_lock:
                print("Network_Thread acquired lock")
                if key == "config":
                    load_config(value)
                    for key, value in config.items():
                        for connection in connections:
                            data = f'{key}: {value}'
                            await connection.send_text(data)
                    print()
                    print('Config Loaded')
                    print()
                if key == "save_config":
                    save_config(value)
                if key in CONFIG_TYPES:
                    if key == "class":
                        try:
                            temp = value.split(',')
                            typecasted_value = [int(v) for v in temp]
                            config[key] = typecasted_value
                            print()
                            print(f'CONFIG UPDATED: config[{key}] = {typecasted_value}')
                            print()
                        except (ValueError, TypeError, AttributeError):
                            # Failed to typecast, use original value
                            print()
                            print('ERROR: TYPECASTING FAILED')
                            print()
                            pass
                    elif CONFIG_TYPES[key] == bool:
                        if value.lower() == 'true':
                            config[key] = True
                            if key == 'raw':
                                debugging = True
                            print()
                            print(f'CONFIG UPDATED: config[{key}] = {config[key]}')
                            print()
                        elif value.lower() == 'false':
                            config[key] = False
                            if key == 'raw':
                                debugging = False
                            print()
                            print(f'CONFIG UPDATED: config[{key}] = {config[key]}')
                            print()
                        else:
                            # Handle case when the value is neither 'true' nor 'false'
                            print()
                            print('ERROR: Invalid boolean value')
                            print()
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
            # Broadcast the received message to all connected clients
            for connection in connections:
                await connection.send_text(data)
    finally:
        # Remove the closed connection from the list
        connections.remove(websocket)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed')
def video_feed():
    # Route for streaming video feed
    return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("standard.png")

if __name__ == "__main__":
    import uvicorn
    import threading
    from capture import capture_frames
    from constants import SOCKET_IP

    capture_thread = threading.Thread(target = capture_frames)
    capture_thread.start()

    uvicorn.run(app, host='0.0.0.0', port=8000)