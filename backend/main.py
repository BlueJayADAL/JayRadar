import threading
import uvicorn
#from network import frontend, network_setup_event, app
from detection import process_frames
from capture import capture_frames#, process_event
from web import app
from constants import SOCKET_IP
from send import send_frames

capture_thread = threading.Thread(target = capture_frames)
capture_thread.start()

#process_event.wait()

#network_thread = threading.Thread(target=frontend)
#network_thread.start()

#network_setup_event.wait()

#send_thread = threading.Thread(target=send_frames)
#send_thread.start()

processing_thread = threading.Thread(target= process_frames)
processing_thread.start()

uvicorn.run(app, host=SOCKET_IP, port=8000)
