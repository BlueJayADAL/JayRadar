import tkinter as tk
import numpy as np
import cv2
import datetime
from PIL import ImageTk, Image
from networktables import NetworkTables

table_name = 'JayRadar'

NetworkTables.initialize()
table = NetworkTables.getTable(table_name)

def value_changed(table, key, value, isNew):
    print()
    print('Update to the JayRadar table found!')
    print(f'Key: {key}, Value: {value}, IsNew: {isNew}')
    print()

table.addEntryListener(value_changed)

# Create the main Tkinter window
window = tk.Tk()
window.title("Video Player")
window.geometry("800x400")

# Create a frame for the left side (dropdown menus and time label)
left_frame = tk.Frame(window)
left_frame.pack(side="left", padx=10, pady=10)

# Create a dropdown menu with the configuration options
config_options = ['Default', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
selected_option = tk.StringVar(window)
selected_option.set(config_options[0])

def config_dropdown_callback(*args):
    selected_config = selected_option.get()
    table.putValue('config', selected_config)
    print("Selected Config:", selected_config)

config_label = tk.Label(left_frame, text="Config:")
config_label.pack(padx=10, pady=10)

config_menu = tk.OptionMenu(left_frame, selected_option, *config_options, command=config_dropdown_callback)
config_menu.pack(padx=10, pady=10)

# Create a dropdown menu with the video URLs
video_urls = ['http://10.1.32.29:8000/nn_feed', 'http://10.1.32.29:8000/video_feed', 'http://10.1.32.29:8000/filtered_feed']
selected_video_url = tk.StringVar(window)
selected_video_url.set(video_urls[0])

url_label = tk.Label(left_frame, text="Video URL:")
url_label.pack(padx=10, pady=10)

url_menu = tk.OptionMenu(left_frame, selected_video_url, *video_urls)
url_menu.pack(padx=10, pady=10)

# Create a label to display the current time
time_label = tk.Label(left_frame, text="")
time_label.pack(pady=10)

# Create a variable to store the checkbox status
checkbox_status = tk.IntVar()
checkbox_status.set(0)  # Set initial status as unchecked (0)

# Create a checkbox
checkbox = tk.Checkbutton(left_frame, text="Video Feed", variable=checkbox_status)
checkbox.pack(padx=10, pady=10)

# Function to update the time label
def update_time():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text="Current Time: " + current_time)
    time_label.after(1000, update_time)  # Update every second

# Create a frame for the right side (video feed)
right_frame = tk.Frame(window)
right_frame.pack(side="right", padx=10, pady=10)

# Create a label to display the video feed
video_label = tk.Label(right_frame)
video_label.pack(padx=10, pady=10)

# Function to update the video feed
running = False
cap = None
current_url = ''

def update_video():
    global cap, current_url, running
    selected_url = selected_video_url.get()
    if checkbox_status.get() == 1:
        active = True
    else:
        active = False

    if active and not running:
        cap = cv2.VideoCapture(selected_url)
        current_url = selected_url
        running = True
    if current_url != selected_url:
        del(cap)
        cap = cv2.VideoCapture(selected_url)
        current_url = selected_url
    if cap.isOpened() and active:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            video_label.config(image=img)
            video_label.image = img

    window.after(30, update_video)  # Update every 30 milliseconds

# Start updating the time label and video feed
update_time()
update_video()

# Run the Tkinter event loop
window.mainloop()
