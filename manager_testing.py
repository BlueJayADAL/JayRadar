from pipelines import PipelineManager
from pipelines.sources import ThreadedSource
from pipelines.outputs import NTDisplay
from interfaces import TerminalUI

if __name__ == "__main__":
    source = ThreadedSource(device=0, windows=True)
    output = NTDisplay()

    manager = PipelineManager(source, output)

    ui = TerminalUI(manager)
    ui.run()