from pipelines import PipelineManager
from pipelines.sources import ThreadedSource
from pipelines.outputs import NTDisplay
if __name__ == "__main__":
    source = ThreadedSource(device=0, windows=True)
    output = NTDisplay()

    manager = PipelineManager(source, output)


    while True:
        command = input("Enter a command: ")
        if command == "quit":
            break
        elif command == "delete":
            index = input("Enter an index: ")
            manager.delete_filter(int(index))
        elif command == "add":
            filter = input("Enter a filter type: ")
            if filter == "hsv":
                index = input("Enter an index: ")
                manager.add_hsv(int(index))
            elif filter == "dl":
                index = input("Enter an index: ")
                manager.add_dl(int(index))
            elif filter == "rgb":
                index = input("Enter an index: ")
                manager.add_rgb(int(index))
        elif command == "update":
            filter = input("Enter a filter type: ")
            key = input("Enter a key: ")
            value = input("Enter a value: ")
            manager.update_configs(filter, key, value)
        elif command == "save":
            file_name = input("Enter a filename: ")
            manager.save_to_json(file_name)
        elif command == "load":
            filename = input("Enter a filename: ")
            manager.load_from_json(filename)

    manager.release()