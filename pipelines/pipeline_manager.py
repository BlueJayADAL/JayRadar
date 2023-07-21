from multiprocessing import Manager, Process, Queue
import json
from .variable_pipeline import VariablePipeline
from .pipes import HSVPipe, RGBPipe, YOLOv8Pipe
from .sources import Source
from .outputs import Output


class PipelineManager:
    """
    PipelineManager class for managing dynamic pipes and configurations in a video processing pipeline.

    This class provides functionality to manage a VariablePipeline object and dynamically add or remove pipes
    at runtime. It uses the multiprocessing module to handle the pipeline as a separate process to avoid blocking
    the main thread. The PipelineManager allows adding HSVFilter, RGBFilter, and DeepLearning pipes, updating
    their configurations, and saving/loading the configurations to/from a JSON file.
    """

    def __init__(self, source: Source, output: Output):
        """
        Initialize the PipelineManager object.

        Args:
            source: An object providing frames for the pipeline.
            output: An object handling the output of the pipeline.

        The PipelineManager object initializes a multiprocessing Manager to handle shared configurations
        for pipes. It creates HSVFilter, RGBFilter, and DeepLearning objects with shared configurations.
        It also initializes a VariablePipeline object to process frames through the pipes dynamically.
        """
        self.manager = Manager()  # Initialize a multiprocessing Manager
        self.configs = {  # Shared configurations for pipes
            "hsv": self.manager.dict({"brightness": 0, "contrast": 1.0, "saturation": 1.0}),
            "rgb": self.manager.dict({"red": 0, "green": 0, "blue": 0}),
            "dl": self.manager.dict({
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
        }

        # Create pipe objects with shared configurations
        self.hsv_pipe = HSVPipe(self.configs["hsv"])
        self.rgb_pipe = RGBPipe(self.configs["rgb"])
        self.dl_pipe = YOLOv8Pipe(self.configs["dl"])

        self.pipe_q = Queue()  # Queue for receiving commands to modify pipes at runtime
        # Initialize the VariablePipeline
        self.pipeline = VariablePipeline(source, output, self.pipe_q)

        self.pipeline_process = Process(
            target=self.pipeline.initialize)  # Process for the pipeline
        self.pipeline_process.start()  # Start the pipeline as a separate process

        self.active_pipes = []  # List to keep track of active pipes

    def delete_index(self, index=0):
        """
        Delete a pipe from the pipeline at the specified index.

        Args:
            index (int): The index of the pipe to be deleted.

        The method adds a "delete" command to the pipe queue, and the pipe will be removed during the pipeline's execution.
        """
        if index > len(self.active_pipes) - 1:
            pass
        else:
            self.pipe_q.put(["delete", index, None])
            del self.active_pipes[index]

    def delete_pipe(self, pipe):
        if pipe in self.active_pipes:
            index = self.active_pipes.index(pipe)
            self.delete_index(index)

    def move_pipe(self, pipe, new_index):
        if pipe in self.active_pipes:
            current_index = self.active_pipes.index(pipe)
            current_pipe = self.active_pipes.pop(current_index)
            self.active_pipes.insert(new_index, current_pipe)
            self.pipe_q.put(["move", current_index, new_index])

    def add_hsv(self, index=0):
        """
        Add an HSVFilter to the pipeline at the specified index.

        Args:
            index (int): The index where the HSVFilter should be inserted.

        The method adds an "add" command with the HSVFilter to the pipe queue, and the pipe will be added during the pipeline's execution.
        """
        if index > len(self.active_pipes):
            index = len(self.active_pipes)
        self.pipe_q.put(["add", index, self.hsv_pipe])
        self.active_pipes.insert(index, "hsv")

    def add_pipe(self, pipe, index=0):
        if index > len(self.active_pipes):
            index = len(self.active_pipes)

        if pipe == "hsv":
            self.pipe_q.put(["add", index, self.hsv_pipe])
            self.active_pipes.insert(index, "hsv")
        elif pipe == "dl":
            self.pipe_q.put(["add", index, self.dl_pipe])
            self.active_pipes.insert(index, "dl")
        elif pipe == "rgb":
            self.pipe_q.put(["add", index, self.rgb_pipe])
            self.active_pipes.insert(index, "rgb")

    def add_dl(self, index=0):
        """
        Add a DeepLearning pipe to the pipeline at the specified index.

        Args:
            index (int): The index where the DeepLearning pipe should be inserted.

        The method adds an "add" command with the DeepLearning pipe to the pipe queue, and the pipe will be added during the pipeline's execution.
        """
        if index > len(self.active_pipes):
            index = len(self.active_pipes)
        self.pipe_q.put(["add", index, self.dl_pipe])
        self.active_pipes.insert(index, "dl")

    def add_rgb(self, index=0):
        """
        Add an RGBFilter to the pipeline at the specified index.

        Args:
            index (int): The index where the RGBFilter should be inserted.

        The method adds an "add" command with the RGBFilter to the pipe queue, and the pipe will be added during the pipeline's execution.
        """
        if index > len(self.active_pipes):
            index = len(self.active_pipes)
        self.pipe_q.put(["add", index, self.rgb_pipe])
        self.active_pipes.insert(index, "rgb")

    def update_configs(self, pipe, key, value):
        """
        Update the configuration of a pipe.

        Args:
            pipe (str): The pipe name (e.g., "hsv", "rgb", "dl").
            key (str): The configuration key to be updated.
            value: The new value for the configuration.

        The method updates the shared configuration of the specified pipe with the new value for the specified key.
        """
        if pipe in self.configs:
            if key in self.configs[pipe]:
                if value is None:
                    self.configs[pipe][key] = None
                else:
                    current_value = self.configs[pipe][key]
                    current_type = type(current_value)

                    if current_value is None:
                        self.configs[pipe][key] = None
                    else:
                        try:
                            self.configs[pipe][key] = current_type(value)
                        except ValueError:
                            print(
                                f"Typecasting failed: '{value}' cannot be converted to {current_type}.")

    def save_to_json(self, file_path):
        """
        Save the current configurations to a JSON file.

        Args:
            file_path (str): The file path where the configurations will be saved.

        The method creates a copy of the shared configurations and saves them to a JSON file with the specified file path.
        """
        copy = {}
        for pipe in self.active_pipes:
            copy[pipe] = self.configs[pipe].copy()

        with open(file_path, 'w') as file:
            json.dump(copy, file, indent=4)

    def load_from_json(self, file_path):
        """
        Load configurations from a JSON file.

        Args:
            file_path (str): The file path of the JSON file to load configurations from.

        The method loads configurations from the specified JSON file and updates the shared configurations accordingly.
        """
        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
                self._rearrange_pipes(loaded_data.keys())
                self._update_configs_recursive(self.configs, loaded_data, "")
        except FileNotFoundError:
            print(f"File {file_path} not found!")

    def _delete_unused_fitlers(self, pipes):
        for pipe in self.active_pipes:
            if pipe not in pipes:
                self.delete_pipe(pipe)
                self._delete_unused_fitlers(pipes)
                break

    def _rearrange_pipes(self, pipes):
        self._delete_unused_fitlers(pipes)
        for i, pipe in enumerate(pipes):
            if pipe in self.active_pipes:
                if self.active_pipes.index(pipe) == i:
                    pass
                else:
                    self.move_pipe(pipe, i)
            else:
                self.add_pipe(pipe, i)

    def _update_configs_recursive(self, current_dict, new_data, pipe):
        """
        Recursively update configurations with new data.

        Args:
            current_dict (dict): The current dictionary to update.
            new_data (dict): The new data to update from.
            pipe (str): The pipe name.

        The method recursively updates the shared configurations with the new data from the JSON file.
        """
        for key, value in new_data.items():
            if isinstance(value, dict):
                if key in current_dict:
                    self._update_configs_recursive(
                        current_dict[key], value, key)
                else:
                    current_dict[key] = value
            else:
                self.update_configs(pipe, key, value)

    def get_active_pipes(self):
        pipes = self.active_pipes
        return pipes

    def get_configs_copy(self):
        rgb_copy = self.configs["rgb"].copy()
        hsv_copy = self.configs["hsv"].copy()
        dl_copy = self.configs["dl"].copy()

        copy = {
            "rgb": rgb_copy,
            "hsv": hsv_copy,
            "dl": dl_copy
        }
        return copy

    def release(self):
        """
        Release resources and terminate the pipeline.

        The method terminates the pipeline process, waits for it to finish, and performs cleanup.
        """
        self.pipeline_process.terminate()
        self.pipeline_process.join()
        self.pipeline.cleanup()
