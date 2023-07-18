from pipelines import PipelineManager
from pipelines.sources import ThreadedSource
from pipelines.outputs import NTDisplay, NTSend
from interfaces import TerminalUI, CV2UI
from multiprocessing import Queue, set_start_method

if __name__ == "__main__":
    set_start_method('spawn')  # Set the start method for multiprocessing
    source = ThreadedSource(device=0, windows=True)
    shared_q = Queue(maxsize=1)
    output = NTSend(shared_q)

    manager = PipelineManager(source, output)

    ui = CV2UI(manager, shared_q)
    ui.run()