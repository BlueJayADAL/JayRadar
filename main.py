from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.sources import ThreadedSource#, Source
from pipelines.outputs import NTDisplay#, Output
from pipelines.filters import HSVFilter, DeepLearning
from webui import WebUI

if __name__ == "__main__":
    set_start_method('spawn')
    
    manager = Manager()

    filters_q = Queue()
    
    shared_config = manager.dict()
    
    shared_config["brightness"] = 0
    shared_config["contrast"] = 1.0
    shared_config["saturation"] = 1.0

    source = ThreadedSource(device=0, windows=True)
    filter1 = HSVFilter(shared_config)
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
            shared_config["brightness"] += 5
        elif keys == "b-":
            shared_config["brightness"] -= 5
        elif keys == "c+":
            shared_config["contrast"] += .1
        elif keys == "c-":
            shared_config["contrast"] -= .1
        elif keys == "s+":
            shared_config["saturation"] += .1
        elif keys == "s-":
            shared_config["saturation"] -= .1
        elif keys == "add":
            filters_q.put(["add", 0, dl_pipe])
        elif keys == "delete":
            filters_q.put(["delete", 0, None])
    
    #my_app = WebUI()
    #my_app.run()

    pipeline_process.terminate()
    pipeline_process.join()
    pipeline.cleanup()

    