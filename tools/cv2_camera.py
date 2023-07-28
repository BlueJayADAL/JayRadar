import cv2
import time
from ultralytics import YOLO

if __name__ == "__main__":
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    model = YOLO('yolov8n.pt')
    while True:
        ret, frame = cap.read()
        if ret:
            results = model(frame)
            annotated_frame = results[0].plot()
            cv2.imshow("cv2 frame", annotated_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        