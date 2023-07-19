from pipelines import PipelineManager

class TerminalUI:
    """
    TerminalUI class for providing a terminal-based user interface to interact with a video processing pipeline.

    This class allows the user to input commands to add and delete filters, update filter configurations,
    and save/load configurations from JSON files. The user can interact with the pipeline managed by a
    PipelineManager object using this terminal user interface.
    """

    def __init__(self, manager: PipelineManager):
        """
        Initialize the TerminalUI object.

        Args:
            manager (PipelineManager): The PipelineManager object used to manage the video processing pipeline.
        """
        self.manager = manager

    def run(self):
        """
        Run the terminal user interface.

        The method provides a loop where the user can enter commands to interact with the video processing pipeline.
        The available commands are "quit," "delete," "add," "update," "save," and "load." The user can quit the
        application with the "quit" command, delete a filter by index with the "delete" command, add a filter with
        the "add" command, update filter configurations with the "update" command, and save/load configurations
        from JSON files with the "save" and "load" commands, respectively.
        """
        while True:
            command = input("Enter a command: ")
            if command == "quit":
                break
            elif command == "delete":
                filter = input("Enter a filter: ")
                self.manager.delete_filter(filter)
            elif command == "add":
                filter_type = input("Enter a filter type: ")
                if filter_type == "hsv":
                    index = input("Enter an index: ")
                    self.manager.add_hsv(int(index))
                elif filter_type == "dl":
                    index = input("Enter an index: ")
                    self.manager.add_dl(int(index))
                elif filter_type == "rgb":
                    index = input("Enter an index: ")
                    self.manager.add_rgb(int(index))
            elif command == "update":
                filter_type = input("Enter a filter type: ")
                key = input("Enter a key: ")
                value = input("Enter a value: ")
                self.manager.update_configs(filter_type, key, value)
            elif command == "save":
                file_name = input("Enter a filename: ")
                self.manager.save_to_json(file_name)
            elif command == "load":
                file_name = input("Enter a filename: ")
                self.manager.load_from_json(file_name)

        self.release()

    def release(self):
        """
        Release resources and terminate the pipeline manager.

        The method releases the resources used by the pipeline manager and terminates the associated pipeline process.
        """
        self.manager.release()
