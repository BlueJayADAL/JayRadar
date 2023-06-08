import tkinter as tk

def update_values():
    model_str = model_entry.get()
    device_str = device_entry.get()
    
    entry_list = []
    entry_list.append(model_str)
    entry_list.append(device_str)
    
    # Print the lists (you can modify this part to store the lists or perform any other desired operations)
    print("List:", entry_list)
    
    # Clear the text boxes
    model_entry.delete(0, tk.END)
    device_entry.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("Model and Device")

# Create the 'Model' label and text box
model_label = tk.Label(window, text="Model:", bg="green")
model_label.pack()
model_entry = tk.Entry(window)  # Set text color to green
model_entry.insert(tk.END, 'n')  # Set default value 'n'
model_entry.pack()

# Create the 'Device' label and text box
device_label = tk.Label(window, text="Device:", bg="green")
device_label.pack()
device_entry = tk.Entry(window)  # Set text color to green
device_entry.insert(tk.END, 'n')  # Set default value 'n'
device_entry.pack()

# Create the 'Update' button
update_button = tk.Button(window, bg="yellow", text="Update", command=update_values)
update_button.pack()

# Start the Tkinter event loop
window.mainloop()