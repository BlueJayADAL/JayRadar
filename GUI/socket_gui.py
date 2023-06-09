import tkinter as tk
import cv2
import socket
import pickle
import struct
from tkinter import Frame, OptionMenu
from PIL import ImageTk, Image
from spinbox import Spinbox
from networktables import NetworkTables
from boundingbox import draw_box_on_frame

# Start Network Tables
NetworkTables.initialize(server="10.4.10.146")
table = NetworkTables.getTable('JayRadar')


# Handle dropdown menu selections
def filter_option_selected(selected_option):
    """Callback function when the filter dropdown is changed"""
    print("Filter Mode: ", selected_option)
    table.putNumber("max_detections", int(selected_option))

def model_option_selected(selected_option):
    """Callback function when the model dropdown is changed"""
    print("Model: ", selected_option)


# Execute the 'Update' button
def update_values():
    print(class_entry.get().split(','))


# Resize frames when to fit the window when the main window is resized
def resize(event):
    """Adjust the size of the frames to fit the window"""
    mainwin.grid_columnconfigure(0, weight=1)
    mainwin.grid_columnconfigure(1, weight=1)
    mainwin.grid_columnconfigure(2, weight=1)
    mainwin.grid_rowconfigure(0, weight=1)

# Display video feed
def show_frames():
    """Retrieve frames from the socket and update the GUI"""
    data = b""
    payload_size = struct.calcsize("Q")
    
    while True:
        # Receive frame size
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Receive frame data
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        objects_key = table.getNumberArray('objects_key', [-1])
        print(objects_key)
        
        for index, key in enumerate(objects_key):
            name = 'object'+str(index)
            box_info = table.getNumberArray(name, [-1])
            print(box_info)
            if box_info[0] == -1:
                break
        
            frame = draw_box_on_frame(frame.copy(), box_info)

        # Convert the color channels from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL ImageTk object
        img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

        cam.imgtk = img  # Keep a reference to the image to prevent garbage collection
        cam.configure(image=img)  # Update the Label widget with the new image

        # Update GUI
        mainwin.update()

    client_socket.close()


# Create the main window
mainwin = tk.Tk()
mainwin.title("Overall GUI")
mainwin.geometry("889x500")
mainwin.resizable(True, True)
mainwin.minsize(width=889, height=500)
mainwin.bind("<Configure>", resize)


# Change the background color of the main window
mainwin.configure(bg="blue")


# Create the internal frames and balance them horizontally
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


# Label frame_1
Tuning = tk.Label(frame_1, bg='grey', text="Tuning", font=("Arial Bold", 30, "underline")).grid(row=0, column=0)


# Label and initialize the confidence threshold spinbox
Conf_Thresh = tk.Label(frame_1, bg='grey', text="Confidence Threshold:", font=("Arial Bold", 12)).grid(row=1, column=0)
Conf_Thresh_Spin = Spinbox(frame_1, name="confidence_threshold", min=0, max=100, increment=1, default_value=table.getNumber("confidence_threshold",50)).grid(row=2, column=0)


# Label and initialize the NMS threshold spinbox
NMS_Thresh = tk.Label(frame_1, bg='grey', text="IOU Threshold:", font=("Arial Bold", 12)).grid(row=3, column=0)
NMS_Thresh_Spin = Spinbox(frame_1, name="iou_threshold", min=0, max=100, increment=1, default_value=table.getNumber("iou_threshold",50)).grid(row=4, column=0)


# Label frame_2
Model_Label = tk.Label(frame_2, bg='grey', text="Model", font=("Arial Bold", 30, "underline")).grid(row=0, column=0, sticky='nsew')


# Label the 'Model' dropdown
model_type = tk.Label(frame_2, bg='grey', text="Model: ", font=("Arial Bold", 12), justify="center").grid(row=1, column=0)


# Create the 'Model' dropdown. Model_Options forms the list of options to choose from
selected_model_option = tk.StringVar(mainwin)
selected_model_option.set("1")  # Set default option
Model_Options = ["1", "2", "3", "4", "5"]
Model_OptionMenu = OptionMenu(frame_2, selected_model_option, *Model_Options, command=model_option_selected)
Model_OptionMenu.grid(row=2, column=0)


# Label and initialize the Max Detections spinbox
Max_Detect = tk.Label(frame_2, bg='grey', text="Max Detections:", font=("Arial Bold", 12)).grid(row=4, column=0)
Max_Detect_Spin = Spinbox(frame_2, name="max_detections", min=0, max=300, increment=1, default_value=table.getNumber("max_detections",10)).grid(row=5, column=0)


# Create a new frame within frame_2 to house resolution options
res_frame = Frame(frame_2, bg='grey')
res_frame.grid(row=3, column=0, pady=20)


# Label the new frame
res_label = tk.Label(res_frame, bg='grey', text="Resolution", font=("Arial Bold", 15, "underline"), justify="center").grid(row=0, column=0)


# Label and initialize the Resolution Width spinbox
res_width = tk.Label(res_frame, bg='grey', text="Width:", font=("Arial Bold", 12)).grid(row=1, column=0)
res_width_spin = Spinbox(res_frame, name="image_size", min=100, max=9999, increment=1, default_value=table.getNumber("image_size",640)).grid(row=2, column=0)


# Label and initialize the Resolution Height spinbox
res_height = tk.Label(res_frame, bg='grey', text="Height:", font=("Arial Bold", 12)).grid(row=3, column=0)
res_height_spin = Spinbox(res_frame, name="image_size", min=100, max=9999, increment=1, default_value=table.getNumber("image_size",640)).grid(row=4, column=0)


# Create the 'Class Filters' label and text box
class_filters = tk.Label(res_frame, bg='grey', text="Width:", font=("Arial Bold", 12)).grid(row=5, column=0)
class_entry = tk.Entry(res_frame)

# Set the initial value to '-1' and place on the grid
class_entry.insert(tk.END, '-1')
class_entry.grid(row=6, column=0, pady=4)


# Create the 'Update' button
update_button = tk.Button(res_frame, text="Update", command=update_values).grid(row=7, column=0)


# Create the widgets in camframe (camera output)
cam = tk.Label(camframe)
cam.grid(row=0, column=0)
calc_disp = tk.Label(camframe, bg='grey', text="Output Information: (x, y, area)", font=("Arial Bold", 12)).grid(row=1, column=0)


# Set up socket connection to receive frames
host = '10.4.10.46'  # Change to the appropriate IP address
port = 9999  # Change to the appropriate port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))


# Start the thread to receive and display frames
show_frames()


# Start the main GUI event loop
mainwin.mainloop()
