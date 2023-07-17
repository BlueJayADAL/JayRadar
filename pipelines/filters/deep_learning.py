from ultralytics import YOLO
import math

class DeepLearning:
    """
    DeepLearning class for performing object detection using YOLO and filtering results.

    This class uses YOLO to perform object detection on frames and filters the results to find the
    closest object to a given target location.
    """

    def __init__(self, config: dict={
        "model": "models/yolov8n.pt",
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
        """
        Initialize the DeepLearning object.

        Args:
            config (dict): A dictionary specifying the configuration parameters for the object detection.
                           The parameters include:
                           - 'model': Path to the YOLO model file. Defaults to "models/yolov8n.pt".
                           - 'tx' and 'ty': Target location coordinates (x, y).
                           - 'conf': Confidence threshold for filtering detections. Defaults to 0.25.
                           - 'iou': IoU (Intersection over Union) threshold for filtering detections. Defaults to 0.7.
                           - 'half': Use half-precision for inference. Defaults to False.
                           - 'ss': Save the result images. Defaults to False.
                           - 'ssd': Save the detection results in text format. Defaults to False.
                           - 'max': Maximum number of detections to keep. Defaults to 7.
                           - 'img': Size of the input image for inference. Defaults to 640.
                           - 'class': List of classes to filter detections. Defaults to None.
        """
        self.config = config  # Dictionary containing the configuration parameters

    def initialize(self):
        """
        Initialize the DeepLearning object.

        This method creates a YOLO object using the specified model file path and stores it in self.model.
        """
        self.model = YOLO(self.config["model"])  # Create a YOLO object using the specified model file

    def _filter_results(self, result):
        """
        Filter YOLO detection results and find the closest box to the target location.

        Args:
            result (YOLODetection): YOLO detection results obtained from the model.predict() method.

        Returns:
            tuple: A tuple containing the information of the closest box and a success flag.
                   If no boxes are found in the result, the success flag is set to False.
                   Otherwise, the tuple contains the information [cx, cy, w, h, id, prob] of the closest box,
                   where:
                   - cx and cy: x and y coordinates of the center of the box.
                   - w and h: width and height of the box.
                   - id: class ID of the box.
                   - prob: confidence score of the box.
        """
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
        """
        Process a frame by performing object detection and filtering results.

        Args:
            frame (numpy.ndarray): The input frame to be processed.
            data (dict): A dictionary containing additional data related to the frame.

        Returns:
            tuple: A tuple containing the annotated frame and the modified data dictionary.

        This method performs object detection using YOLO on the input frame. It then filters the detection
        results to find the closest box to the target location (tx, ty) specified in the configuration.
        The information of the closest box is stored in the data dictionary with keys 'tx', 'ty', 'tw', 'th',
        'id', and 'tc'. If no boxes are found in the detection results, the 'te' key in the data dictionary
        is set to False. Otherwise, the 'te' key is set to True to indicate a successful detection.
        The annotated frame obtained from YOLO's plot() method is returned along with the modified data dictionary.
        """
        results = self.model.predict(
            frame,
            conf=self.config["conf"],
            iou=self.config["iou"],
            half=self.config["half"],
            save=self.config["ss"],
            save_txt=self.config["ssd"],
            max_det=self.config["max"],
            classes=self.config["class"],
            imgsz=self.config["img"],
            verbose=False
        )

        result, success = self._filter_results(results[0])

        annotated_frame = results[0].plot()

        if success:
            data['tx'], data['ty'], data['tw'], data['th'], data['id'], data['tc'] = result
            data['te'] = True
        else:
            data['te'] = False

        return annotated_frame, data

    def release(self):
        """
        Release resources used by the DeepLearning object.

        This method is currently empty as the DeepLearning class does not require any resource release.
        """
        pass
