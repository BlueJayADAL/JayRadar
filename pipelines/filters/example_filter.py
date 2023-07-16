class ExampleFilter:
    def __init__(self, config:dict={"example": 0}):
        #Only use this to save the input, do not initialize objects here.
        #Variables initialized here will have to be sent to the new process
        self.config = config

    def initialize(self):
        #Use this to initalize objects. This will be called once a new process is started.
        pass

    def process_frame(self, frame, data):
        #Do some thing to the frame and data.
        return frame, data

    def release(self):
        pass