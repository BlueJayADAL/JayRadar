import cv2
from ultralytics import YOLO



model = YOLO('yolov8n.pt')

results = model.predict(source=0, stream=True)

for result in results:
    annotated_frame = result.plot()
    cv2.imshow("YOLO", annotated_frame)
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break