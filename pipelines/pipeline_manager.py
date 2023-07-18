from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.filters import HSVFilter, RGBFilter, DeepLearning
import json

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

        self.hsv_fitler = HSVFilter(self.configs["hsv"])
        self.rgb_filter = RGBFilter(self.configs["rgb"])
        self.dl_filter = DeepLearning(self.configs["dl"])

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
                    
    def save_to_json(self, file_path):

        rgb_copy = self.configs["rgb"].copy()
        hsv_copy = self.configs["hsv"].copy()
        dl_copy = self.configs["dl"].copy()

        copy = {
            "rgb": rgb_copy,
            "hsv": hsv_copy,
            "dl": dl_copy
        }


        with open(file_path, 'w') as file:
            json.dump(copy, file, indent=4)

    def load_from_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
                self.update_configs_recursive(self.configs, loaded_data, "")
        except FileNotFoundError:
            print(f"File {file_path} not found!")

        

    def update_configs_recursive(self, current_dict, new_data, filter):
        for key, value in new_data.items():
            if isinstance(value, dict):
                if key in current_dict:
                    self.update_configs_recursive(current_dict[key], value, key)
                else:
                    current_dict[key] = value
            else:
                self.update_configs(filter, key, value)

    def release(self):
        self.pipeline_process.terminate()
        self.pipeline_process.join()
        self.pipeline.cleanup()