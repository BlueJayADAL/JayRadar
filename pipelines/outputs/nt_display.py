import cv2
import time
from networktables import NetworkTables

class NTDisplay:
    def __init__(self, server:str='10.1.32.27', table:str='JayRadar', verbose=False):
        self.server = server
        self.table_name = table
        self.running = False
        self.verbose = verbose

    def initialize(self):
        NetworkTables.initialize(server=self.server)
        self.table = NetworkTables.getTable(self.table_name)

    def send_frame(self, frame, data):

        for key, value in data.items():
            self.table.putValue(key, value)
            if self.verbose:
                print(f"Placed on table: /Jayradar/{key}/{value}")

        cv2.imshow('Output', frame)
        final_time = time.time()
        
        end_to_end_time = round(final_time - data["timestamp"], 5)
        if end_to_end_time < .0001:
            end_to_end_time = .0001

        self.table.putNumber("IterationTime", end_to_end_time)
        self.table.putNumber("FPS", (1/end_to_end_time))

        if self.verbose:
            print(f"End to end time: {end_to_end_time} | FPS: {1/end_to_end_time}")
    
    def release(self):
        cv2.destroyAllWindows()
