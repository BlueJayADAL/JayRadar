import cv2


class WebCamera:
    def __init__(self, q_out, device:int=0,):
        self.device = device
        self.q_out = q_out

    def start_capture(self):
        self.cap = cv2.VideoCapture(self.device, cv2.CAP_DSHOW)  # Assuming camera index 0

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            # Put the frame into the output queue
            self.q_out.put(frame)

        # Release the camera
        self.cap.release()

        # Signal the end of frames by putting None in the output queue
        self.q_out.put(None)
