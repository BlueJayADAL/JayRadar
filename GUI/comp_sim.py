import tkinter as tk
import numpy as np
import cv2
import datetime
from PIL import ImageTk, Image
from networktables import NetworkTables

table_name = 'JayRadar'

NetworkTables.initialize()
table = NetworkTables.getTable(table_name)

cap = None
jayradar_ip = '10.1.32.29'

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
video_urls = ['none', 'nn_feed', 'video_feed', 'filtered_feed']
selected_video_url = tk.StringVar(window)
selected_video_url.set(video_urls[0])

url_label = tk.Label(left_frame, text="Video URL:")
url_label.pack(padx=10, pady=10)

def url_dropdown_callback(*args):
    global cap, jayradar_ip
    selected_endpoint = selected_video_url.get()
    if selected_endpoint == 'none':
        del(cap)
        cap = None
    else:
        url = f'http://{jayradar_ip}:8000/{selected_endpoint}'
        del(cap)
        cap = cv2.VideoCapture(url)


url_menu = tk.OptionMenu(left_frame, selected_video_url, *video_urls, command=url_dropdown_callback)
url_menu.pack(padx=10, pady=10)

# Create a label to display the current time
time_label = tk.Label(left_frame, text="")
time_label.pack(pady=10)

# Function to update the time label
def update_time():
    tx = table.getValue('tx', -1)
    ty = table.getValue('tx', -1)
    tw = table.getValue('tx', -1)
    th = table.getValue('tx', -1)
    ta = table.getValue('tx', -1)
    tc = table.getValue('tx', -1)
    detection_info = f"tx: {tx} | ty: {ty} | tw: {tw} | th: {th} | ta: {ta} | tc: {tc}"
    time_label.config(text=detection_info)
    time_label.after(30, update_time)  # Update every second

# Create a frame for the right side (video feed)
right_frame = tk.Frame(window)
right_frame.pack(side="right", padx=10, pady=10)

# Create a label to display the video feed
video_label = tk.Label(right_frame)
video_label.pack(padx=10, pady=10)

# Function to update the video feed

def update_video():
    global cap
    if cap is not None:
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
