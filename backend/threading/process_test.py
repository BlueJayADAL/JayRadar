import cv2
from ultralytics import YOLO
from constants import MODEL_NAME, NT_SERVER_IP
from capture import frame_queue
from networktables import NetworkTables
from network import config, nt_lock
import time

def test_process():
    """
    Function to process frames from the frame queue using YOLOv8.
    """
    # Load the YOLOv8 model
    model = YOLO(MODEL_NAME)

    NetworkTables.initialize(NT_SERVER_IP)

    # Retrieve the JayRadar table for us to use
    nt = NetworkTables.getTable("JayRadar")

    while True:

        if frame_queue:
            frame = frame_queue[-1]  # Get the newest frame from the deque

            with nt_lock:
                print("Process_Thread acquired lock")
                conf = config['conf'] / 100
                iou = config['iou'] / 100
                half = config['half']
                save = config['ss']
                save_conf = config['ssd']
                max_det = config['max']
                image_size = config['img']
                classes = config['class']
                print("Process_Thread released lock")

            time.sleep(2)
            # If the first index of classes is -1
            print(f'Max_det: {max_det}')
            print(f'conf: {conf}')
            if (classes[0]==-1):
                # Process the frame using YOLOv8 without class filter
                results = model.predict(
                    frame.copy(),
                    conf=conf,
                    iou=iou,
                    #half=half,
                    #device=device,
                    save=save,
                    save_conf=save_conf,
                    max_det=max_det,
                    imgsz = image_size
                    )
            else:
            # Otherwise, process the frame using YOLOv8 with class filter
                results = model.predict(
                    frame.copy(),
                    conf=conf,
                    iou=iou,
                    #half=half,
                    #device=device,
                    save=save,
                    save_conf=save_conf,
                    max_det=max_det,
                    classes=classes,
                    imgsz = image_size
                )
            result = results[0]  # Get the detection results from the first image in the batch
            
            objects = []

            for index, box in enumerate(result.boxes):
                name = 'object'+str(index)
                cx, cy, w, h = [
                    x for x in box.xywh[0].tolist()
                ]  # Extract the bounding box coordinates and round them
                class_id = box.cls[0].item()  # Get the class ID of the detected object
                prob = round(box.conf[0].item(), 2)  # Get the detection probability
                output = [cx, cy, w, h, prob]  # Append the bounding box information to the output list
                objects.append(float(class_id))
                nt.putNumberArray(name, output)
            nt.putNumberArray('objects_key', objects)
            
            # Annotate and display the frame for testing, will be removed in final version
            annotated_frame = results[0].plot()

            
            cv2.imshow('YOLOv8 Inference', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break