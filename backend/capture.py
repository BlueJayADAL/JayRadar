import cv2
import threading
from collections import deque
import numpy as np

# Maximum number of frames to keep in the deque
MAX_FRAMES = 5

# Deque to share frames between threads
frame_queue = deque(maxlen=MAX_FRAMES)

# Event to control frame processing
process_event = threading.Event()

cam_lock = threading.Lock()

cam_config = {
    "cam": 0,
    "auto_exp": False,
    "exp": -5,
    "bri": 0,
    "cont": 1.0,
    "red": 0,
    "gre": 0,
    "blu": 0
}

def get_available_cameras():
    available_cameras = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            available_cameras.append(cap)
        index += 1
    return available_cameras

# Thread function to capture video frames and add them to the frame queue
def capture_frames():
    global cam_config
    """
    Function to capture video frames and add them to the frame queue.
    """
    cameras = get_available_cameras()
    cap = cameras[0]
    contrast = 1.0
    brightness = 0
    exposure = -5
    red_value = 0 
    blue_value = 0  
    green_value = 0 
    auto_exposure = False

    print("Camera Aquired")

    while cap.isOpened():
        success, frame = cap.read()
        if cap != cameras[cam_config['cam']]:
            cap = cameras[cam_config['cam']]
        if contrast != cam_config['cont']:
            contrast = cam_config['cont']
            print(f'Contrast = {contrast}')
        if auto_exposure != cam_config['auto_exp']:
            auto_exposure = cam_config['auto_exp']
            if auto_exposure:
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
        if not auto_exposure and exposure != cam_config['exp']:
            exposure = cam_config['exp']
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
            print(f'Exposure = {cap.get(cv2.CAP_PROP_EXPOSURE)}')
        if brightness != cam_config['bri']:
            brightness = cam_config['bri']
            print(f'Brightness = {brightness}')
        if red_value != cam_config['red']:
            red_value = cam_config['red']
            print(f'Red = {red_value}')
        if green_value != cam_config['gre']:
            green_value = cam_config['gre']
            print(f'Green = {green_value}')
        if blue_value != cam_config['blu']:
            blue_value = cam_config['blu']
            print(f'Blue = {blue_value}')

        if success:
            adjusted_frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
            adjusted_frame[:, :, 2] = np.clip(adjusted_frame[:, :, 2] + red_value, 0, 255).astype(np.uint8)  # Adjust red channel
            adjusted_frame[:, :, 0] = np.clip(adjusted_frame[:, :, 0] + blue_value, 0, 255).astype(np.uint8)  # Adjust blue channel
            adjusted_frame[:, :, 1] = np.clip(adjusted_frame[:, :, 1] + green_value, 0, 255).astype(np.uint8)  # Adjust green channel

            # Put frame in the deque for processing
            frame_queue.append(adjusted_frame)
            process_event.set()  # Set the event to resume frame processing

    cap.release()
