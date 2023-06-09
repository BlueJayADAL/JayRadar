import socket
import pickle
import struct
import threading
from constants import SOCKET_IP
from capture import frame_queue, process_event




# Thread function to send frames over a socket connection
def send_frames():
    """
    Function to send frames over a socket connection.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = SOCKET_IP
    port = 9999
    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(1)

    while True:
        client_socket, addr = server_socket.accept()

        while True:
            process_event.wait()  # Wait for the event to be set, so we know there's a frame
            process_event.clear()  # Clear the event, it will be set again next

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
