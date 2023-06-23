# NetworkTables IP address
NT_SERVER_IP = "10.1.80.32" 
#Laptop: 10.4.10.146
#Flex: 10.1.80.32
#Mypc: 10.1.32.27

TABLE_NAME = "JayRadar"

# Socket IP address
SOCKET_IP = "10.1.80.32" 
#Recomputer: "10.4.10.46" 

# MODEL NAME string
MODEL_NAME = "yolov8n.pt"

# MAX FRAMES int
MAX_FRAMES = 5

# WEBPAGE HTML FILE
HTML_PAGE = "test.html"

# DEFAULT TUNING VALUES
DEFAULT_CONF = 25
DEFAULT_IOU = 70
DEFAULT_PRECISION = False      #Not very useful
DEFAULT_PROCESSOR = "cpu"           #Not very useful
DEFAULT_SS = False
DEFAULT_SSD = False
DEFAULT_MAX_DETECT = 5
DEFAULT_CLASSES = [-1]
DEFAULT_IMGSZ = 640

CONFIG_TYPES = {
    "conf": int,
    "iou": int,
    "half": bool,
    "ss": bool,
    "ssd": bool,
    "max": int,
    "img": int,
    "class": list
}