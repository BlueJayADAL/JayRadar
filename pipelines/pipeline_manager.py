from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.filters import HSVFilter, RGBFilter, DeepLearning

class PipelineManager():
    def __init__(self, source, output):
        set_start_method('spawn')
        self.manager = Manager()

        dl_config = self.manager.dict({
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
            })

        hsv_config = self.manager.dict({"brightness": 0, "contrast": 1.0, "saturation": 1.0})

        rgb_config = self.manager.dict({"red": 0, "green": 0, "blue": 0})

        self.configs = {
            "rgb": rgb_config,
            "hsv": hsv_config,
            "dl": dl_config
        }

        self.hsv_fitler = HSVFilter(hsv_config)
        self.rgb_filter = RGBFilter(rgb_config)
        self.dl_filter = DeepLearning(dl_config)

        self.filter_q = Queue()
        self.pipeline = VariablePipeline(source, output, self.filter_q)

        self.pipeline_process = Process(target=self.pipeline.initialize)
        self.pipeline_process.start()

        self.active_filters = []

    def delete_filter(self, index):
        if index > len(self.active_filters) - 1:
            pass
        else:
            self.filter_q.put(["delete", index, None])
            del self.active_filters[index]

    def add_hsv(self, index):
        if index > len(self.active_filters):
            index = len(self.active_filters)
        self.filter_q.put(["add", index, self.hsv_fitler])
        self.active_filters.insert(index, "hsv")
    
    def add_dl(self, index):
        if index > len(self.active_filters):
            index = len(self.active_filters)
        self.filter_q.put(["add", index, self.dl_filter])
        self.active_filters.insert(index, "dl")
    
    def add_rgb(self, index):
        if index > len(self.active_filters):
            index = len(self.active_filters)
        self.filter_q.put(["add", index, self.rgb_filter])
        self.active_filters.insert(index, "rgb")
    
    def update_configs(self, filter, key, value):
        if filter in self.configs:
            
            if key in self.configs[filter]:

                if value is None:
                    self.configs[filter][key] = None
                
                current_value = self.configs[filter][key]
                current_type= type(current_value)

                if current_value is None:
                    self.configs[filter][key] = None

                else:
                    try:
                        self.configs[filter][key] = current_type(value)
                    except ValueError:
                        print(f"Typecasting failed: '{value}' cannot be converted to {current_type}.")
    
    def release(self):
        self.pipeline_process.terminate()
        self.pipeline_process.join()
        self.pipeline.cleanup()