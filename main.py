import multiprocessing as mp
from pipelines import Pipeline
from pipelines.sources import Source, ThreadedSource
from pipelines.outputs import Output, NTDisplay
from pipelines.filters import HSVFilter, DeepLearning

if __name__ == "__main__":
    mp.set_start_method('spawn')
    
    manager = mp.Manager()
    
    shared_config = manager.dict()
    
    shared_config["brightness"] = 0
    shared_config["contrast"] = 1.0
    shared_config["saturation"] = 1.0

    source = ThreadedSource(device=0, windows=True)
    filter1 = HSVFilter(shared_config)
    #dl_pipe = DeepLearning()
    output = NTDisplay(verbose=False)
    pipeline = Pipeline(source, output, filter1,)

    pipeline_process = mp.Process(target=pipeline.initialize)
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

    pipeline_process.terminate()
    pipeline_process.join()
    pipeline.cleanup()

    