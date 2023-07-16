import cv2
import multiprocessing as mp
from ultralytics import YOLO
from threaded_cam import ThreadedCamera
import requests

def capture_and_display(process_id):
    cap = cv2.VideoCapture(process_id)  # Use process_id as the camera index
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(f"Process {process_id}", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
def deep_learning(process_id):
    cap = cv2.VideoCapture(process_id)
    model = YOLO('yolov8n.pt')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow(f"Deep Learning Process {process_id}", annotated_frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def threaded_learning(process_id):
    cap = ThreadedCamera(device=process_id)
    cap.start_capture()
    model = YOLO('yolov8n.pt')
    
    while True:
        frame = cap.get_frame()
        if frame is not None:
            results = model(frame)
            annotated_frame = results[0].plot()
            cv2.imshow(f"Threaded Learning Process {process_id}", annotated_frame)
            if cv2.waitKey(1) == ord('q'):
                break
        
    cap.stop_capture()
    cv2.destroyAllWindows()
    
    
def capture_and_post(process_id):
    cap = cv2.VideoCapture(process_id)  # Use process_id as the camera index
    url = f"https://localhost:8000/video{process_id}"
    print(f"makeing capture available to {url}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to bytes
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # Send HTTP POST request to the desired URL
        response = requests.post(url, data=img_bytes)

        

    cap.release()

if __name__ == '__main__':
    mp.set_start_method('spawn')
    process1 = mp.Process(target=capture_and_display, args=(1,))
    process2 = mp.Process(target=capture_and_post, args=(2,))

    process1.start()
    process2.start()

    input("Press Enter to stop...")

    process1.terminate()
    process2.terminate()

    process1.join()
    process2.join()
