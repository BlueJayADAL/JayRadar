import cv2
import socket
import pickle
import struct
import threading
from collections import deque
from ultralytics import YOLO

# Maximum number of frames to keep in the deque
MAX_FRAMES = 5

# Deque to share frames between threads
frame_queue = deque(maxlen=MAX_FRAMES)

# Event to control frame processing
process_event = threading.Event()

# Thread function to capture video frames and add them to the frame queue
def capture_frames():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            # Put frame in the deque for processing
            frame_queue.append(frame)
            process_event.set()  # Set the event to resume frame processing

            cv2.imshow('Capturing Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()

# Thread function to process frames from the frame queue
def process_frames():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    while True:
        process_event.wait()  # Wait for the event to be set
        process_event.clear()  # Clear the event

        if frame_queue:
            frame = frame_queue[-1]  # Get the newest frame from the deque

            # Process the frame using YOLOv8
            results = model.predict(frame.copy())
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow('YOLOv8 Inference', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Thread function to send frames over a socket connection
def send_frames():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(1)
    print('LISTENING AT:', socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        while True:
            if frame_queue:
                frame = frame_queue[-1]  # Get the newest frame from the deque

                # Convert frame to bytes
                data = pickle.dumps(frame)
                message = struct.pack('Q', len(data)) + data

                # Send frame to client
                try:
                    client_socket.sendall(message)
                except socket.error:
                    client_socket.close()
                    break

    server_socket.close()

# Start the capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

# Start the processing thread
process_thread = threading.Thread(target=process_frames)
process_thread.start()

# Start the frame sending thread
send_thread = threading.Thread(target=send_frames)
send_thread.start()

# Wait for threads to finish
capture_thread.join()
process_thread.join()
send_thread.join()

cv2.destroyAllWindows()
