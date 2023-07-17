from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.sources import ThreadedSource#, Source
from pipelines.outputs import NTDisplay#, Output
from pipelines.filters import HSVFilter, RGBFilter, DeepLearning
from webui import WebUI

if __name__ == "__main__":
    set_start_method('spawn')
    
    manager = Manager()

    filters_q = Queue()
    
    hsv_config = manager.dict()
    
    hsv_config["brightness"] = 0
    hsv_config["contrast"] = 1.0
    hsv_config["saturation"] = 1.0

    rgb_config = manager.dict()
    
    rgb_config["red"] = 15
    rgb_config["green"] = 27
    rgb_config["blue"] = -23

    source = ThreadedSource(device=0, windows=True)
    hsv_pipe = HSVFilter(hsv_config)
    rgb_pipe = RGBFilter(rgb_config)
    dl_pipe = DeepLearning()
    output = NTDisplay(verbose=False)
    pipeline = VariablePipeline(source, output, filters_q,)

    pipeline_process = Process(target=pipeline.initialize)
    pipeline_process.start()

    
    while True:
        keys = input("Enter a command: ")
        if keys == "q":
            break
        elif keys == "b+":
            hsv_config["brightness"] += 5
        elif keys == "b-":
            hsv_config["brightness"] -= 5
        elif keys == "c+":
            hsv_config["contrast"] += .1
        elif keys == "c-":
            hsv_config["contrast"] -= .1
        elif keys == "s+":
            hsv_config["saturation"] += .1
        elif keys == "s-":
            hsv_config["saturation"] -= .1
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

    