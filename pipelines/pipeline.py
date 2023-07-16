import cv2

class Pipeline:
    def __init__(self, source, output, *filters):
        self.source = source
        self.output = output
        self.filters = filters

    def initialize(self):
        self.source.initialize()
        self.output.initialize()
        for pipe in self.filters:
            pipe.initialize()
        self.run()

    def run(self):

        while True:
            frame, data = self.source.get_frame()
            if frame is None:
                break

            for pipe in self.filters:
                frame, data = pipe.process_frame(frame, data)

            self.output.send_frame(frame, data)
            
            cv2.waitKey(1)

        self.cleanup()

    def cleanup(self):
        self.source.release()
        self.output.release()
        for pipe in self.filters:
            pipe.release()
