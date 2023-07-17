# Trying to make a more proper user interface

class TerminalUI:
    def __init__(self, configs:dict):
        self.configs = configs

    def update_hsv(self, key, value):
        if "hsv" in self.configs:
            if key in self.configs["hsv"]:
                self.configs["hsv"][key] = value

    def run(self):
        while True:
            keys = input("Enter a command: ")
            if keys == "q":
                break
            elif keys == "hsv":
                key = input("Enter a key: ")
                value = input("Enter a value: ")
                value = float(value)
                self.update_hsv(key, value)