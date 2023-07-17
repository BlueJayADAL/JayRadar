from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.sources import ThreadedSource#, Source
from pipelines.outputs import NTDisplay#, Output
from pipelines.filters import HSVFilter, RGBFilter, DeepLearning
from interfaces import WebUI

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

    
    while True:
        keys = input("Enter a command: ")
        if keys == "q":
            break
        elif keys == "b+":
            complete_configs["hsv"]["brightness"] += 5
            print(f'Brightness = {hsv_config["brightness"]}')
        elif keys == "b-":
            hsv_config["brightness"] -= 5
            print(f'Brightness = {hsv_config["brightness"]}')
        elif keys == "c+":
            dl_config["conf"] += .05
            print(f'Confidence = {dl_config["conf"]}')
        elif keys == "c-":
            dl_config["conf"] -= .05
            print(f'Confidence = {dl_config["conf"]}')
        elif keys == "s+":
            hsv_config["saturation"] += .1
            print(f'Saturation = {hsv_config["saturation"]}')
        elif keys == "s-":
            hsv_config["saturation"] -= .1
            print(f'Saturation = {hsv_config["saturation"]}')
        elif keys == "r+":
            rgb_config["red"] += 5
        elif keys == "r-":
            rgb_config["red"] -= 5
        elif keys == "g+":
            rgb_config["green"] += 5
        elif keys == "g-":
            rgb_config["green"] -= 5
        elif keys == "l+":
            rgb_config["blue"] += 5
        elif keys == "l-":
            rgb_config["blue"] -= 5
        elif keys == "dl":
            filters_q.put(["add", 0, dl_pipe])
        elif keys == "rgb":
            filters_q.put(["add", 0, rgb_pipe])
        elif keys == "hsv":
            filters_q.put(["add", 0, hsv_pipe])
        elif keys == "delete":
            filters_q.put(["delete", 0, None])
    
    #my_app = WebUI()
    #my_app.run()

    pipeline_process.terminate()
    pipeline_process.join()
    pipeline.cleanup()

    