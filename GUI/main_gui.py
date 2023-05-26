import tkinter as tk
from tkinter import Frame, OptionMenu
import cv2
from PIL import ImageTk, Image
from spinbox import Spinbox

def filter_option_selected(selected_option):
    """Callback function when the filter dropdown is changed"""
    print("Filter Mode: ", selected_option)

def model_option_selected(selected_option):
    """Callback function when the model dropdown is changed"""
    print("Model: ", selected_option)

def resize(event):
    """Adjust the size of the frames to fit the window"""
    mainwin.grid_columnconfigure(0, weight=1)
    mainwin.grid_columnconfigure(1, weight=1)
    mainwin.grid_columnconfigure(2, weight=1)
    mainwin.grid_rowconfigure(0, weight=1)

def show_frames():
    """Retrieve frames from the camera and update the GUI"""
    ret, frame = cap.read()  # Read frame from the camera
    if ret:
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally

        # Convert the color channels from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL ImageTk object
        img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

        cam.imgtk = img  # Keep a reference to the image to prevent garbage collection
        cam.configure(image=img)  # Update the Label widget with the new image

    cam.after(10, show_frames)  # Schedule the next frame update after 30 milliseconds

# Create the main window
mainwin = tk.Tk()
mainwin.title("Overall GUI")
mainwin.geometry("889x500")
mainwin.resizable(True, True)
mainwin.minsize(width=889, height=500)
mainwin.bind("<Configure>", resize)

# Change the background color of the main window to green
mainwin.configure(bg="blue")

# Create the internal frames
frame_1 = Frame(mainwin, bg='grey')
frame_1.grid(row=0, column=0, sticky="nsew", padx=1)
frame_1.grid_columnconfigure(0, weight=1)

frame_2 = Frame(mainwin, bg='grey')
frame_2.grid(row=0, column=1, sticky="nsew", padx=1)
frame_2.grid_columnconfigure(0, weight=1)

camframe = Frame(mainwin, bg='grey')
camframe.grid(row=0, column=2, sticky="nw", padx=1)
camframe.grid_columnconfigure(0, weight=1)
camframe.grid_rowconfigure(0, weight=1)

# Configure the layout of the main window
mainwin.grid_columnconfigure(0, weight=1, minsize=180)
mainwin.grid_columnconfigure(1, weight=1, minsize=160)
mainwin.grid_columnconfigure(2, weight=2)
mainwin.grid_rowconfigure(0, weight=1, minsize=500)

# Create the widgets in frame_1 ('Tuning')
Tuning = tk.Label(frame_1, bg='grey', text="Tuning", font=("Arial Bold", 30, "underline")).grid(row=0, column=0)

Conf_Thresh = tk.Label(frame_1, bg='grey', text="Confidence Threshold:", font=("Arial Bold", 12)).grid(row=1, column=0)
Conf_Thresh_Spin = Spinbox(frame_1, min=0, max=100, increment=1, default_value=50).grid(row=2, column=0)

NMS_Thresh = tk.Label(frame_1, bg='grey', text="NMS Threshold:", font=("Arial Bold", 12)).grid(row=3, column=0)
NMS_Thresh_Spin = Spinbox(frame_1, min=0, max=100, increment=1, default_value=50).grid(row=4, column=0)

filter_type = tk.Label(frame_1, bg='grey', text="Filter mode: ", font=("Arial Bold", 12), justify="center").grid(row=5, column=0)
selected_filter_option = tk.StringVar(mainwin)
selected_filter_option.set("Closest")  # Set default option
Filter_Options = ["Closest", "Highest Confidence"]
Filter = OptionMenu(frame_1, selected_filter_option, *Filter_Options, command=filter_option_selected).grid(row=6, column=0)

# Create the widgets in frame_2 ('Model')
Model_Label = tk.Label(frame_2, bg='grey', text="Model", font=("Arial Bold", 30, "underline")).grid(row=0, column=0, sticky = 'nsew')

model_type = tk.Label(frame_2, bg='grey', text="Model: ", font=("Arial Bold", 12), justify="center").grid(row=1, column=0)

selected_model_option = tk.StringVar(mainwin)
selected_model_option.set("1")  # Set default option
Model_Options = ["1", "2", "3", "4", "5"]
Model_OptionMenu = OptionMenu(frame_2, selected_model_option, *Model_Options, command=model_option_selected)
Model_OptionMenu.grid(row=2, column=0)

res_frame = Frame(frame_2, bg='grey')
res_frame.grid(row=3, column=0, pady=20)

res_label = tk.Label(res_frame, bg='grey', text="Resolution", font=("Arial Bold", 15, "underline"), justify="center").grid(row=0, column=0)

res_width = tk.Label(res_frame, bg='grey', text="Width:", font=("Arial Bold", 12)).grid(row=1, column=0)
res_width_spin = Spinbox(res_frame, min=100, max=9999, increment=1, default_value=400).grid(row=2, column=0)

res_height = tk.Label(res_frame, bg='grey', text="Height:", font=("Arial Bold", 12)).grid(row=3, column=0)
res_height_spin = Spinbox(res_frame, min=100, max=9999, increment=1, default_value=400).grid(row=4, column=0)

# Create the widgets in camframe (camera output)
cam = tk.Label(camframe)
cam.grid(row=0, column=0)
calc_disp = tk.Label(camframe, bg='grey', text="Output Information: (x, y, area)", font=("Arial Bold", 12)).grid(row=1, column=0, sticky = 'n')

# Open the video capture
cap = cv2.VideoCapture(0)

# Start displaying frames
show_frames()

# Start the GUI event loop
mainwin.mainloop()