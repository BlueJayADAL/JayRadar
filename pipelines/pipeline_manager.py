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

    def release(self):
        self.pipeline_process.terminate()
        self.pipeline_process.join()
        self.pipeline.cleanup()