from ultralytics import YOLO
import math
import cv2
from networktables import NetworkTables


class DeepLearning:
    def __init__(self, q_in, q_out, pipeline_config, model='yolov8n.pt'):
        self.model = YOLO(model)
        self.q_in = q_in
        self.q_out = q_out
        self.config = pipeline_config

        #NetworkTables.initialize(server = '10.1.32.27')

        #self.table = NetworkTables.getTable("JayRadar")

    def filter_send_crosshair(self, result, tx, ty):
        #if not result.boxes:
        #    self.table.putBoolean('te', False)

        closest_box = None
        min_distance = math.inf

        for box in result.boxes:
            cx, cy, w, h = [round(x) for x in box.xywh[0].tolist()]

            # Find the closest point on the outside of the box
            closest_x = max(cx - w / 2, min(tx, cx + w / 2))
            closest_y = max(cy - h / 2, min(ty, cy + h / 2))

            distance = math.sqrt((closest_x - tx)**2 + (closest_y - ty)**2)

            if distance < min_distance:
                min_distance = distance
                a = w*h
                id = box.cls
                prob = box.conf
                closest_box = [cx, cy, w, h, a, id, prob]
        """
        self.table.putBoolean('te', True)
        self.table.putNumber('tx', closest_box[0])
        self.table.putNumber('ty', closest_box[1])
        self.table.putNumber('tw', closest_box[2])
        self.table.putNumber('th', closest_box[3])
        self.table.putNumber('id', closest_box[4])
        self.table.putNumber('tp', closest_box[5])

        """ 
    def start_pipeline(self):
        frame = None
        while True:
            if self.q_in:
                print('Starting detection loop')
                frame = self.q_in[-1]

                if frame is None:
                    print('Breaking detection loop, frame is none')
                    cv2.destroyAllWindows()
                    break
                    
                cv2.imshow('Detection Loop Pre', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

                results = self.model.predict(
                    frame, 
                    imgsz=640, 
                    conf=self.config['conf'],
                    )
                #self.filter_send_crosshair(results[0], 320, 240)
                annotated_frame = results[0].plot()
                self.q_out.append(annotated_frame)
            else:
                print('no frame')