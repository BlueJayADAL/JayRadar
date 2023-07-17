# Trying to make a more proper user interface

class TerminalUI:
    def __init__(self, configs:dict):
        self.configs = configs

    def update_hsv(self, key, value):
        if "hsv" in self.configs:
            if key in self.configs["hsv"]:
                self.configs["hsv"][key] = value

    def update_configs(self, filter, key, value):
        if filter in self.configs:
            if key in self.configs[filter]:
                current_type= type(self.configs[filter][key])
                
                try:
                    self.configs[filter][key] = current_type(value)
                except ValueError:
                    print(f"Typecasting failed: '{value}' cannot be converted to {current_type}.")

    def run(self):
        while True:
            keys = input("Enter a command: ")
            if keys == "q":
                break
            filter = input("Enter a filter: ")
            key = input("Enter a key: ")
            value = input("Enter a value: ")
            self.update_configs(filter, key, value)