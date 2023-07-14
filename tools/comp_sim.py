import tkinter as tk
import cv2
from PIL import ImageTk, Image
from networktables import NetworkTables

table_name = 'JayRadar'

NetworkTables.initialize()
table = NetworkTables.getTable(table_name)

cap = None
jayradar_ip = '10.1.32.29'
tx = -1
ty = -1
tw = -1
th = -1
ta = -1
tc = -1
avgdelay = -1
delay = -1

def value_changed(table, key, value, isNew):
    global tx, ty, tw, th, ta, tc, avgdelay, delay
    if key == 'tx':
        tx = round(value, 3)
    elif key == 'ty':
        ty = round(value, 3)
    elif key == 'tw':
        tw = round(value, 3)
    elif key == 'th':
        th = round(value, 3)
    elif key == 'ta':
        ta = round(value, 3)
    elif key == 'tc':
        tc = round(value, 3)
    elif key == 'delay':
        delay = round(value*1000, 1)
    elif key == 'avgdelay':
        avgdelay = round(value*1000, 1)
    detection_info = f"tc: {tc} | delay: {delay}ms | avgdelay: {avgdelay}ms | avgFPS: {round(1000/avgdelay, 1)}"
    time_label.config(text=detection_info)

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
time_label = tk.Label(left_frame, text="No updates to netorktables")
time_label.pack(pady=10)

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
update_video()

# Run the Tkinter event loop
window.mainloop()
