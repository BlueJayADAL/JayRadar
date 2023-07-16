from ultralytics import YOLO

class DeepLearning:
    def __init__(self, model="yolov8n.pt"):
        self.model_name = model

    def initialize(self):
        self.model = YOLO(self.model_name)

    def process_frame(self, frame, data):
        results = self.model.predict(frame, verbose=False)
        annotated_frame = results[0].plot()
        data['result'] = results[0]
        return annotated_frame, data
    
    def release(self):
        pass
