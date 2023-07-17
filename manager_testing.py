from pipelines import PipelineManager
from pipelines.sources import ThreadedSource
from pipelines.outputs import NTDisplay
if __name__ == "__main__":
    source = ThreadedSource(device=0, windows=True)
    output = NTDisplay(verbose=False)

    manager = PipelineManager(source, output)

    input("Hit Enter to stop...")

    manager.release()