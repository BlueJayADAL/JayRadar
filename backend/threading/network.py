from networktables import NetworkTables
import json
import threading
import uvicorn
import time
from web import app
from constants import SOCKET_IP, NT_SERVER_IP, CONFIG_TYPES, TABLE_NAME

network_setup_event = threading.Event()

NetworkTables.initialize(NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

# Lock for accessing NetworkTables vairables. 
# This ensures that no other threads have access when this thread is trying to access them
nt_lock = threading.Lock()

def save_config(filename, config):
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)

def load_config(filename, config):
    try:    
        with open(filename, 'r') as file:
            new_config = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return config
    typecasted_config = {}
    for key, value in CONFIG_TYPES.items():
        if key == "class":
            try:
                typecasted_value = [int(v) for v in value]
                typecasted_config[key] = typecasted_value
            except (ValueError, TypeError):
                # Failed to typecast, use original value
                typecasted_config[key] = config[key]
        else:
            try:
                typecasted_value = CONFIG_TYPES[key](value)
                typecasted_config[key] = typecasted_value
            except (ValueError, TypeError):
                # Failed to typecast, use original value
                typecasted_config[key] = config[key]
    
        nt.putValue(key, config[key])


    return typecasted_config
config = {  
        "conf": 25,
        "iou": 70,
        "half": False,
        "ss": False,
        "ssd": False,
        "max": 5,
        "img": 480,
        "class": [
            -1
        ]
    }
config = load_config('default.json', config)
def frontend():
    global config
    def value_changed(table, key, value, isNew):
        global config
        print()
        print('UPDATE TO JAYRADAR FOUND')
        print(f"Value changed: {key} = {value}")
        print()
        with nt_lock:
            print("Network_Thread acquired lock")
            if key in CONFIG_TYPES.items():
                if key == "class":
                    try:
                        typecasted_value = [int(v) for v in value]
                        config[key] = typecasted_value
                        print()
                        print('CLASSES UPDATED')
                        print()
                    except (ValueError, TypeError):
                        # Failed to typecast, use original value
                        print()
                        print('ERROR: TYPECASTING FAILED')
                        print()
                        pass
                else:
                    try:
                        typecasted_value = CONFIG_TYPES[key](value)
                        config[key] = typecasted_value
                        print()
                        print('CONFIG UPDATED')
                        print()
                    except (ValueError, TypeError):
                        # Failed to typecast, use original value
                        print()
                        print('ERROR: TYPECASTING FAILED')
                        print()
                        pass
            print("Network_Thread released lock")
    
    time.sleep(1)
    nt.addEntryListener(value_changed)
    network_setup_event.set()
    i=0
    time.sleep(10)
    while True:
        nt.putNumber('conf',i)
        time.sleep(3)
        i+= 1
    #uvicorn.run(app, host=SOCKET_IP, port=8000)