import threading
import uvicorn
from network import frontend, network_setup_event, app
from process_test import test_process
from capture import capture_frames, process_event
#from send import send_frames

capture_thread = threading.Thread(target = capture_frames)
capture_thread.start()

#process_event.wait()

network_thread = threading.Thread(target=frontend)
network_thread.start()

network_setup_event.wait()

#send_thread = threading.Thread(target=send_frames)
#send_thread.start()

processing_thread = threading.Thread(target= test_process)
processing_thread.start()

uvicorn.run(app, host="10.1.32.27", port=8000)
