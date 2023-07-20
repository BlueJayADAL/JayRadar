from pipelines import PipelineManager
from pipelines.sources import ThreadedSource
from pipelines.outputs import NTDisplay, NTSend
from interfaces import TerminalUI, CV2UI, WebUI
from multiprocessing import Queue, set_start_method

if __name__ == "__main__":
    set_start_method('spawn')  # Set the start method for multiprocessing
    source = ThreadedSource(device=0, windows=True)
    shared_q = Queue(maxsize=1)
    output = NTDisplay()

    manager = PipelineManager(source, output)

    # manager.add_dl(0)
    manager.add_hsv(0)
    manager.add_rgb(0)

    ui = TerminalUI(manager)
    ui.run()
