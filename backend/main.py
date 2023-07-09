import threading
import uvicorn
from detection import process_frames
from capture import capture_frames
from web import app, load_config
from send import send_filtered_results
from constants import SOCKET_IP
import argparse

parser = argparse.ArgumentParser(description="Run the webserver on the localhost (Only visiable to the local machine)")
parser.add_argument("-l", "--localhost", action="store_true", help="Run the webserver on the localhost (Only visiable to the local machine)")

args = parser.parse_args()



capture_thread = threading.Thread(target = capture_frames)
capture_thread.start()

processing_thread = threading.Thread(target= process_frames)
processing_thread.start()

results_thread = threading.Thread(target= send_filtered_results)
results_thread.start()

load_config('default')

if args.localhost:
    uvicorn.run(app, host='0.0.0.0', port=8000)
else:
    uvicorn.run(app, host= SOCKET_IP, port=8000)

