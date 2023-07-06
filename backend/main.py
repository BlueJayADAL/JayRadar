import threading
import uvicorn
from detection import process_frames
from capture import capture_frames
from web import app
from send import send_filtered_results
from constants import SOCKET_IP


capture_thread = threading.Thread(target = capture_frames)
capture_thread.start()

processing_thread = threading.Thread(target= process_frames)
processing_thread.start()

results_thread = threading.Thread(target= send_filtered_results)
results_thread.start()

uvicorn.run(app, host=SOCKET_IP, port=8000)
