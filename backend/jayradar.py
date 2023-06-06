import socket
import cv2
import pickle
import struct
import numpy as np
from PIL import Image
from ultralytics import YOLO
from networktables import NetworkTables

class JayRadar:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.host_ip = "10.4.10.46"
        self.port = 9999
        self.socket_address = (self.host_ip, self.port)

        self.model = YOLO("yolov8n.pt")
        self.table = NetworkTables.getTable("JayRadar")

    def detect_objects_on_image(self, confidence_threshold=50):
        confidence_threshold = self.table.getNumber("confidence_threshold", 50)
        iou_threshold = self.table.getNumber("iou_threshold", 50)
        half_precision = self.table.getBoolean("half_precision", False)
        processor = self.table.getString("device", "0")
        screenshot = self.table.getBoolean("screenshot", False)
        screenshot_data = self.table.getBoolean("screenshot_data", False)
        max_detections = int(self.table.getNumber("max_detections", 3))
        detected_classes = self.table.getNumberArray("classes", [0])
        display_boxes = self.table.getBoolean("display_boxes", True)

        self.results = self.model.predict(
            self.buf,
            conf=confidence_threshold / 100,
            iou=iou_threshold / 100,
            half=half_precision,
            device=processor,
            save=screenshot,
            save_conf=screenshot_data,
            max_det=max_detections,
            classes=detected_classes
        )
        result = self.results[0]
        output = []
        if display_boxes:
            self.buf = self.results[0].plot()

        for box in result.boxes:
            x1, y1, x2, y2 = [
                round(x) for x in box.xyxy[0].tolist()
            ]
            class_id = box.cls[0].item()
            prob = round(box.conf[0].item(), 2)
            output.append([
                x1, y1, x2, y2, result.names[class_id], prob
            ])
            self.table.putNumber("x1", x1)
            self.table.putNumber("y1", y1)
            self.table.putNumber("x2", x2)
            self.table.putNumber("y2", y2)
        return output

    def send_detected_objects(self):
        csi_camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if csi_camera.isOpened():
            video_source = csi_camera
        else:
            video_source = cv2.VideoCapture(0)

        while True:
            client_socket, addr = self.server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                while True:
                    ret, self.buf = video_source.read()
                    self.buf = Image.fromarray(cv2.cvtColor(self.buf, cv2.COLOR_BGR2RGB))
                    results = self.detect_objects_on_image(self.buf)
                    frame_pil_with_boxes = self.buf.copy()
                    frame_with_boxes = cv2.cvtColor(np.array(frame_pil_with_boxes), cv2.COLOR_RGB2BGR)
                    a = pickle.dumps(frame_with_boxes)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

    def start(self):
        self.server_socket.bind(self.socket_address)
        self.server_socket.listen(5)
        print("LISTENING AT:", self.socket_address)
        NetworkTables.initialize(server="10.1.80.32")
        self.send_detected_objects()

if __name__ == '__main__':
    radar = JayRadar()
    radar.start()
