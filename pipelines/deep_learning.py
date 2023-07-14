from ultralytics import YOLO


class DeepLearning:
    def __init__(self, q_in, q_out, model='yolov8n.pt'):
        self.model = YOLO(model)
        self.q_in = q_in
        self.q_out = q_out

    def start_pipeline(self):
        frame = None
        while True:
            frame = self.q_in.get()

            if frame is not None:
                results = self.model.predict(frame, imgsz=320)
                annotated_frame = results[0].plot()
                self.q_out.put(annotated_frame)