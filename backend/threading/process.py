import cv2
import threading
from ultralytics import YOLO
from networktables import NetworkTables
from constants import MODEL_NAME, NT_SERVER_IP
from capture import frame_queue, process_event

def process_frames():
    """
    Function to process frames from the frame queue using YOLOv8.
    """
    # Load the YOLOv8 model
    model = YOLO(MODEL_NAME)
    # Initialize NetworkTables
    NetworkTables.initialize(NT_SERVER_IP)

    # Retrieve the JayRadar table for us to use
    nt = NetworkTables.getTable("JayRadar")

    # Lock for accessing NetworkTables vairables. 
    # This ensures that no other threads have access when this thread is trying to access them
    nt_lock = threading.Lock()

    # Variables to store the configuration values
    # TODO: pull these from a default pipeline/config
    confidence_threshold = 50
    iou_threshold = 50
    half_precision = False      #Not very useful
    processor = "cpu"           #Not very useful
    screenshot = False
    screenshot_data = False
    max_detections = 5
    detected_classes = [-1]
    
    image_size = 640

    def value_changed(table, key, value, isNew):
        """
        Callback function to handle value changes in NetworkTables.
        This section looks really intimidating at first glance, but I promise it's not!
        First, we will start by grabbing the default variables from an outside context.
        Then we will 
        There is a ton of typecasting and error handling, so it doesn't look pretty
        """
        # TODO: Add a pipeline/config listener and saver.

        # Grab the variables from outside the function definition explicitly
        nonlocal confidence_threshold, iou_threshold, half_precision, processor, screenshot, screenshot_data, max_detections, detected_classes, image_size
        
        # With the lock, update the variables. This makes sure that no other threads can access it.
        with nt_lock:
            # Check the variables in order
            if key == "confidence_threshold":
                # Try typecasting to the correct type for the model. This is done because during testing NT was accidently posting strings
                try:
                    confidence_threshold = int(value) # Could be replaced with float. Choose int because there's no need for that precision
                # If it fails, just don't update the value.
                except ValueError:
                    pass
            # Check for the next variable, and repeat.
            elif key == "iou_threshold":
                try:
                    iou_threshold = int(value)
                except ValueError:
                    pass
            elif key == "half_precision":
                try:
                    half_precision = bool(value)
                except ValueError:
                    pass
            elif key == "device":
                if (value == "cpu"):
                    processor = value
                else:
                    try:
                        processor = int(value)
                    except:
                        pass
            elif key == "screenshot":
                try:
                    screenshot = bool(value)
                except ValueError:
                    pass
            elif key == "screenshot_data":
                try:
                    screenshot_data = bool(value)
                except ValueError:
                    pass
            elif key == "max_detections":
                try:
                    max_detections = int(value)
                except ValueError:
                    pass
            elif key == "image_size":
                try:
                    image_size = int(value)
                except ValueError:
                    pass
            elif key == "classes":
                # Make sure it's a list first
                if isinstance(value, list):  
                    # Create/Wipe updated_classes   
                    updated_classes = []        
                    #Iterate through the value list
                    for update in value:
                        # Try to make the update an Integer and add it to updated classes
                        try:
                            updated_classes.append(int(update))
                        # If it can't be an integer
                        except ValueError:
                        # Do nothing
                            pass
                    # Set detected_classes equal to updated classes
                    detected_classes = updated_classes
   

    # Add an entry listener to monitor value changes, with the above callback function exectuted on change
    nt.addEntryListener(value_changed)  # This will run in the background.

    while True:

        if frame_queue:
            frame = frame_queue[-1]  # Get the newest frame from the deque

            with nt_lock:
                conf = confidence_threshold / 100
                iou = iou_threshold / 100
                half = half_precision
                device = processor
                save = screenshot
                save_conf = screenshot_data
                max_det = max_detections
                classes = detected_classes

            # If the first index of classes is -1
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