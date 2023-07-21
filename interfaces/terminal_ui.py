from pipelines import PipelineManager


class TerminalUI:
    """
    TerminalUI class for providing a terminal-based user interface to interact with a video processing pipeline.

    This class allows the user to input commands to add and delete pipes, update pipe configurations,
    and save/load configurations from JSON files. The user can interact with the pipeline managed by a
    PipelineManager object using this terminal user interface.
    """  # noqa: E501

    def __init__(self, manager: PipelineManager):
        """
        Initialize the TerminalUI object.

        Args:
            manager (PipelineManager): The PipelineManager object used to manage the video processing pipeline.
        """  # noqa: E501
        self.manager = manager

    def run(self):
        """
        Run the terminal user interface.

        The method provides a loop where the user can enter commands to interact with the video processing pipeline.
        The available commands are "quit," "delete," "add," "update," "save," and "load." The user can quit the
        application with the "quit" command, delete a pipe by index with the "delete" command, add a pipe with
        the "add" command, update pipe configurations with the "update" command, and save/load configurations
        from JSON files with the "save" and "load" commands, respectively.
        """  # noqa: E501
        while True:
            command = input("Enter a command: ")
            if command == "quit":
                break
            elif command == "delete":
                pipe = input("Enter a pipe: ")
                self.manager.delete_pipe(pipe)
            elif command == "add":
                pipe_type = input("Enter a pipe type: ")
                if pipe_type == "hsv":
                    index = input("Enter an index: ")
                    self.manager.add_hsv(int(index))
                elif pipe_type == "dl":
                    index = input("Enter an index: ")
                    self.manager.add_dl(int(index))
                elif pipe_type == "rgb":
                    index = input("Enter an index: ")
                    self.manager.add_rgb(int(index))
            elif command == "update":
                pipe_type = input("Enter a pipe type: ")
                key = input("Enter a key: ")
                value = input("Enter a value: ")
                self.manager.update_configs(pipe_type, key, value)
            elif command == "save":
                file_name = input("Enter a filename: ")
                self.manager.save_to_json(file_name)
            elif command == "load":
                file_name = input("Enter a filename: ")
                self.manager.load_from_json(file_name)
            elif command == "move":
                pipe = input("Enter a pipe: ")
                index = input("Enter an index to move to: ")
                self.manager.move_pipe(pipe, int(index))

        self.release()

    def release(self):
        """
        Release resources and terminate the pipeline manager.

        The method releases the resources used by the pipeline manager and terminates the associated pipeline process.
        """  # noqa: E501
        self.manager.release()
