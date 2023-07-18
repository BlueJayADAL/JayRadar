from multiprocessing import Manager, Process, set_start_method, Queue
from pipelines import VariablePipeline
from pipelines.filters import HSVFilter, RGBFilter, DeepLearning
import json

class PipelineManager:
    """
    PipelineManager class for managing dynamic filters and configurations in a video processing pipeline.

    This class provides functionality to manage a VariablePipeline object and dynamically add or remove filters
    at runtime. It uses the multiprocessing module to handle the pipeline as a separate process to avoid blocking
    the main thread. The PipelineManager allows adding HSVFilter, RGBFilter, and DeepLearning filters, updating
    their configurations, and saving/loading the configurations to/from a JSON file.
    """

    def __init__(self, source, output):
        """
        Initialize the PipelineManager object.

        Args:
            source: An object providing frames for the pipeline.
            output: An object handling the output of the pipeline.

        The PipelineManager object initializes a multiprocessing Manager to handle shared configurations
        for filters. It creates HSVFilter, RGBFilter, and DeepLearning objects with shared configurations.
        It also initializes a VariablePipeline object to process frames through the filters dynamically.
        """
        self.manager = Manager()  # Initialize a multiprocessing Manager
        self.configs = {  # Shared configurations for filters
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

        # Create filter objects with shared configurations
        self.hsv_filter = HSVFilter(self.configs["hsv"])
        self.rgb_filter = RGBFilter(self.configs["rgb"])
        self.dl_filter = DeepLearning(self.configs["dl"])

        self.filter_q = Queue()  # Queue for receiving commands to modify filters at runtime
        self.pipeline = VariablePipeline(source, output, self.filter_q)  # Initialize the VariablePipeline

        self.pipeline_process = Process(target=self.pipeline.initialize)  # Process for the pipeline
        self.pipeline_process.start()  # Start the pipeline as a separate process

        self.active_filters = []  # List to keep track of active filters

    def delete_filter(self, index):
        """
        Delete a filter from the pipeline at the specified index.

        Args:
            index (int): The index of the filter to be deleted.

        The method adds a "delete" command to the filter queue, and the filter will be removed during the pipeline's execution.
        """
        if index > len(self.active_filters) - 1:
            pass
        else:
            self.filter_q.put(["delete", index, None])
            del self.active_filters[index]

    def add_hsv(self, index):
        """
        Add an HSVFilter to the pipeline at the specified index.

        Args:
            index (int): The index where the HSVFilter should be inserted.

        The method adds an "add" command with the HSVFilter to the filter queue, and the filter will be added during the pipeline's execution.
        """
        if index > len(self.active_filters):
            index = len(self.active_filters)
        self.filter_q.put(["add", index, self.hsv_filter])
        self.active_filters.insert(index, "hsv")

    def add_dl(self, index):
        """
        Add a DeepLearning filter to the pipeline at the specified index.

        Args:
            index (int): The index where the DeepLearning filter should be inserted.

        The method adds an "add" command with the DeepLearning filter to the filter queue, and the filter will be added during the pipeline's execution.
        """
        if index > len(self.active_filters):
            index = len(self.active_filters)
        self.filter_q.put(["add", index, self.dl_filter])
        self.active_filters.insert(index, "dl")

    def add_rgb(self, index):
        """
        Add an RGBFilter to the pipeline at the specified index.

        Args:
            index (int): The index where the RGBFilter should be inserted.

        The method adds an "add" command with the RGBFilter to the filter queue, and the filter will be added during the pipeline's execution.
        """
        if index > len(self.active_filters):
            index = len(self.active_filters)
        self.filter_q.put(["add", index, self.rgb_filter])
        self.active_filters.insert(index, "rgb")

    def update_configs(self, filter, key, value):
        """
        Update the configuration of a filter.

        Args:
            filter (str): The filter name (e.g., "hsv", "rgb", "dl").
            key (str): The configuration key to be updated.
            value: The new value for the configuration.

        The method updates the shared configuration of the specified filter with the new value for the specified key.
        """
        if filter in self.configs:
            if key in self.configs[filter]:
                if value is None:
                    self.configs[filter][key] = None
                else:
                    current_value = self.configs[filter][key]
                    current_type = type(current_value)

                    if current_value is None:
                        self.configs[filter][key] = None
                    else:
                        try:
                            self.configs[filter][key] = current_type(value)
                        except ValueError:
                            print(f"Typecasting failed: '{value}' cannot be converted to {current_type}.")

    def save_to_json(self, file_path):
        """
        Save the current configurations to a JSON file.

        Args:
            file_path (str): The file path where the configurations will be saved.

        The method creates a copy of the shared configurations and saves them to a JSON file with the specified file path.
        """
        rgb_copy = self.configs["rgb"].copy()
        hsv_copy = self.configs["hsv"].copy()
        dl_copy = self.configs["dl"].copy()

        copy = {
            "rgb": rgb_copy,
            "hsv": hsv_copy,
            "dl": dl_copy
        }

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
                self.update_configs_recursive(self.configs, loaded_data, "")
        except FileNotFoundError:
            print(f"File {file_path} not found!")

    def update_configs_recursive(self, current_dict, new_data, filter):
        """
        Recursively update configurations with new data.

        Args:
            current_dict (dict): The current dictionary to update.
            new_data (dict): The new data to update from.
            filter (str): The filter name.

        The method recursively updates the shared configurations with the new data from the JSON file.
        """
        for key, value in new_data.items():
            if isinstance(value, dict):
                if key in current_dict:
                    self.update_configs_recursive(current_dict[key], value, key)
                else:
                    current_dict[key] = value
            else:
                self.update_configs(filter, key, value)

    def release(self):
        """
        Release resources and terminate the pipeline.

        The method terminates the pipeline process, waits for it to finish, and performs cleanup.
        """
        self.pipeline_process.terminate()
        self.pipeline_process.join()
        self.pipeline.cleanup()
