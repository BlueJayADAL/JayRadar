from ultralytics import YOLO
import math

class DeepLearning:
    def __init__(self, model="yolov8n.pt"):
        self.model_name = model

    def initialize(self):
        self.model = YOLO(self.model_name)

    def _filter_results(self, result, tx=320, ty=240):
        if not result.boxes:
            return None, False
        closest_box = None
        min_distance = math.inf

        for box in result.boxes:
            cx, cy, w, h = [round(x, 4) for x in box.xywh[0].tolist()]
            distance = math.sqrt((cx - tx)**2 + (cy - ty)**2)

            if distance < min_distance:
                min_distance = distance
                id = float(box.cls)
                prob = float(box.conf)
                closest_box = [cx, cy, w, h, id, prob]

        return closest_box, True

    def process_frame(self, frame, data):
        results = self.model.predict(frame, verbose=False)
        
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
