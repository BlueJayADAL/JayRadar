from threaded_cam import ThreadedCamera
import cv2
import time
from ultralytics import YOLO
if __name__ == "__main__":
    cap = ThreadedCamera()

    cap.start_capture()
    model = YOLO('yolov8n.pt')

    while True:
        frame = cap.get_frame()

        if frame is not None:

            results = model(frame)

            annotated_frame = results[0].plot()

            cv2.imshow("Threaded capture", annotated_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    cv2.destroyAllWindows()
    cap.stop_capture()