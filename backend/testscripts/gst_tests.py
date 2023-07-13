import cv2
from ultralytics import YOLO

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink DROP=1"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
    
    #"v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink"


def show_camera():

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(sensor_id=1, flip_method=2))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0,flip_method=2), cv2.CAP_GSTREAMER)
    
#    model = YOLO('yolov8n.pt')


    while video_capture.isOpened():
        ret_val, frame = video_capture.read()
        if ret_val:
#            results = model.predict(frame)
#            result = results[0]
#            annotated_frame = result.plot()
            annotated_frame = frame.copy()

            cv2.imshow("CSI Camera", annotated_frame)

            keyCode = cv2.waitKey(1) & 0xFF
            # Stop the program on the 'q' key
            if keyCode == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    show_camera()
