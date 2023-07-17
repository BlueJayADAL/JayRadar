from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.sources import ThreadedSource#, Source
from pipelines.outputs import NTDisplay#, Output
from pipelines.filters import HSVFilter, RGBFilter, DeepLearning
from interfaces import TerminalUI#, WebUI

if __name__ == "__main__":
    set_start_method('spawn')
    
    manager = Manager()

    filters_q = Queue()

    dl_config = manager.dict({
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

    hsv_config = manager.dict({"brightness": 0, "contrast": 1.0, "saturation": 1.0})

    rgb_config = manager.dict({"red": 0, "green": 0, "blue": 0})

    complete_configs = {
        "rgb": rgb_config,
        "hsv": hsv_config,
        "dl": dl_config
    }

    source = ThreadedSource(device=0, windows=True)
    hsv_pipe = HSVFilter(hsv_config)
    rgb_pipe = RGBFilter(rgb_config)
    dl_pipe = DeepLearning(dl_config)
    output = NTDisplay(verbose=False)
    pipeline = VariablePipeline(source, output, filters_q, rgb_pipe, hsv_pipe, dl_pipe)

    pipeline_process = Process(target=pipeline.initialize)
    pipeline_process.start()
    
    ui = TerminalUI(complete_configs, filters_q)
    ui.run()

    pipeline_process.terminate()
    pipeline_process.join()
    pipeline.cleanup()

    