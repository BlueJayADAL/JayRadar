import multiprocessing as mp
from pipelines import VariablePipeline
from pipelines.sources import Source, ThreadedSource
from pipelines.outputs import Output, NTDisplay
from pipelines.filters import HSVFilter, DeepLearning

class Manager():
    def __init__(self, pipeline:VariablePipeline):
        mp.set_start_method('spawn')
        self.pipeline = pipeline