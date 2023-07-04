# JayRadar_Backend

JayRadar_Backend is a Python implementation of YoloV8 for the FIRST Robotics Comeptition.

## Dependencies

To install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run JayRadar:

```bash
python3 main.py
```

## Layout

```
/ (backend)
├── configs
│ ├── [0-9].json
│ └── default.json
├── static
│ ├── static.js
│ └── styles.css
└── templates
│ └── index.html
├── Standard.png
├── capture.py
├── constants.py
├── detection.py
├── filter.py
├── main.py
├── send.py
├── web.py
└── web.py
```

### Configs

This folder contains the configs for each of the tunable configs 0-9, and a default config.

### Static

This folder contains the JavaSript and CSS needed to run the web GUI.

### Templates

This folder contains index.html The html file rendered in the web GUI

### Capture.py

This file contains all of the python relating to the camera. The capture_frames function defined here is targeted as a thread.

### Detection.py

This file contains all of the python relating to the Neural Detection. The process_frames function defined here is targeted as a thread.
This file currently contains the active backend networktabels implementation

### Filters.py

This file contains the filters that are overlayed after the detections for the Neural detection. There are a few examples, and teams can make more or change the example implementations. These can be called in deteciton.py's process_frames function on every iteration to filter out certain options.

### Send.py

This file contains all of the code relating to the socket for VideoFeed. This is used in the Socket GUI for tunning. The send_frames function defined here can be targeted as a thread to enable this option.

### Web.py

This file contains all of the code relating to the on-demand web GUI server. The app created here is run in the main file after defining the other threads.
It should not effect performance to run this, but may effect performance when visiting the site. This effect should be minimal.

### Constants.py

This file contains the constants for the backend. Each constant has a breif description above it.
Make sure to change the SOCKET_IP to the hosts IP address, and NT_SERVER_IP to the Networktable server's host (typically the robrio).
You can also change the TABLE_NAME variable from here. This will change the table that the data from your coprocessor is posted to, and listening for updates from. The default is JayRadar, but teams may choose to rename this for some extra customization.

### Main.py

This file is the main file that imports the functions targeted by the threads and runs them. It also imports the app from web.py and runs that.

### MISC

Standard.png is the icon displayed for the webpage.
frc7ng.pt is our PyTorch model trained on google Colab for FRC Charged Up.
yolov8n.pt is the provided yolov8 nano model used for testing and troubleshooting.
The testscripts folder contains scripts that are used in testing and may be useful for troubleshooting
