import tkinter as tk

def spinbox_change(name, change):
    print(name,"changed to: ",change)

class Spinbox(tk.Frame):
    def __init__(self, parent, name, default_value=50, min=0, max=100, increment=1, **kwargs):
        super().__init__(parent, **kwargs)

        self.name = name

        self.min = min
        self.max = max
        self.increment = increment

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT)

        self.subtract_button = tk.Button(self.button_frame, text="-", command=self.subtract, bg='grey')
        self.subtract_button.pack(side=tk.LEFT)

        self.entry = tk.Entry(self, width=8)
        self.entry.pack(side=tk.LEFT)
        self.set(default_value)

        self.buttonplus_frame = tk.Frame(self)
        self.buttonplus_frame.pack(side=tk.RIGHT)

        self.add_button = tk.Button(self.buttonplus_frame, text="+", command=self.add, bg='grey')
        self.add_button.pack(side=tk.RIGHT)

        self.entry.bind("<Return>", self.on_enter)
    
    def subtract(self):
        current_value = self.get()
        new_value = current_value - self.increment
        if new_value >= self.min:
            self.set(new_value)

    def add(self):
        current_value = self.get()
        new_value = current_value + self.increment
        if new_value <= self.max:
            self.set(new_value)

    def get(self):
        try:
            value = int(self.entry.get())
            if self.min <= value <= self.max:
                return value
        except ValueError:
            pass
        return self.min

    def set(self, value):
        if self.min <= value <= self.max:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(value))
            spinbox_change(self.name,int(value))

    def on_enter(self, event):
        current_value = self.get()
        spinbox_change(self.name, current_value)
