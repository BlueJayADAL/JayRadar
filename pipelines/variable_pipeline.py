from pipelines import Pipeline

class VariablePipeline(Pipeline):
    def __init__(self, source, output, config, edit_q, *filters):
        self.source = source
        self.output = output
        self.config = config
        self.edit_q = edit_q
        self.filters = list(filters)

    def add_pipe(self):
        pass
    
    def pop_pipe(self):
        pass
    