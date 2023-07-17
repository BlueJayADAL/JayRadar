from pipelines import Pipeline
import cv2

class VariablePipeline(Pipeline):
    def __init__(self, source, output, filter_q, *filters):
        super().__init__(source, output, *filters)
        self.filters = list(self.filters)
        self.filter_q = filter_q

    def check_q(self):
        while not self.filter_q.empty():
            command, index, filter = self.filter_q.get()

            if command == "add":
                self.add_filter(filter, index=index)
            elif command == "delete":
                self.del_filter(index)
    
    def add_filter(self, filter, index=0):
        if index > self.num_filters:
                index = self.num_filters
        filter.initialize()
        self.filters.insert(index, filter)
        self.num_filters += 1
    
    def remove_filter(self, filter):
        try:
            self.filters.remove(filter)
        except ValueError:
            print("Remove_filter function failed in Variable_Pipeline")
    
    def del_filter(self, index:int=0):
        if index > (self.num_filters-1):
            return False
        else:
            del self.filters[index]
            self.num_filters -= 1
    
    def run(self):

        while True:
            self.check_q()
            frame, data = self.source.get_frame()
            if frame is None:
                break

            for filter in self.filters:
                frame, data = filter.process_frame(frame, data)

            self.output.send_frame(frame, data)
            
            cv2.waitKey(1)

        self.cleanup()
    