from ultralytics import YOLO
import math

class DeepLearning:
    def __init__(self, config: dict={
        "model": "yolov8n.pt",
        "tx": 320,
        "ty": 240,
        "conf": .25,
        "iou": .7,
        "half": False,
        "ss": False,
        "ssd": False,
        "max": 7,
        "img": 640,
        "class": None
        }):

        self.config = config

    def initialize(self):
        self.model = YOLO(self.config["model"])

    def _filter_results(self, result):

        if not result.boxes:
            return None, False
        
        closest_box = None
        min_distance = math.inf

        for box in result.boxes:
            cx, cy, w, h = [round(x, 4) for x in box.xywh[0].tolist()]
            distance = math.sqrt((cx - self.config["tx"])**2 + (cy - self.config["ty"])**2)

            if distance < min_distance:
                min_distance = distance
                id = float(box.cls)
                prob = float(box.conf)
                closest_box = [cx, cy, w, h, id, prob]

        return closest_box, True

    def process_frame(self, frame, data):
        
        results = self.model.predict(
            frame,
            conf=self.config["conf"],
            iou=self.config["iou"],
            half=self.config["half"],
            save=self.config["ss"],
            save_txt=self.config["ssd"],
            max_det=self.config["max"],
            classes=self.config["class"],
            imgsz = self.config["img"],
            verbose=False
        )
        
        result, success = self._filter_results(results[0])
        
        annotated_frame = results[0].plot()
        
        if success:
            data['tx'], data['ty'], data['tw'], data['th'], data['id'], data['tc'] = result
            data['te'] = True
        else:
            data['te'] = True
        
        return annotated_frame, data
    
    def release(self):
        pass
