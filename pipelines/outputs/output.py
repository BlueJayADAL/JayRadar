import cv2
import time

class Output:
    def __init__(self):
        pass

    def initialize(self):
        pass

    def send_frame(self, frame, data):

        cv2.imshow('Output', frame)
        final_time = time.time()

        end_to_end_time = round(final_time - data["timestamp"], 5)
        if end_to_end_time < .0001:
            end_to_end_time = .0001

        print(f"End to end time: {end_to_end_time} | FPS: {1/end_to_end_time}")
    
    def release(self):
        cv2.destroyAllWindows()
