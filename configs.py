import json

def save_dictionary_to_json(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file, indent=4)

def load_dictionary_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


if __name__ == "__main__":

    # Save a dictionary to a JSON file
    
    header = {
        "Filters": ["hsv", "rgb", "dl"]
    }

    hsv = {"brightness": 0, "contrast": 1.0, "saturation": 1.0}

    rgb = {"red": 0, "green": 0, "blue": 0}
    
    dl = {
        "model": "models/yolov8n.pt",
        "tx": 320,
        "ty": 240,
        "conf": .25,
        "iou": .7,
        "half": False,
        "ss": False,
        "ssd": False,
        "max": 7,
        "img": 640,
        "class": None
        }
    
    data = {
        "Header": header,
        "hsv": hsv,
        "rgb": rgb,
        "dl": dl
    }
    save_dictionary_to_json(data, 'data.json')

    # Load a dictionary from a JSON file
    loaded_data = load_dictionary_from_json('data.json')
    print(loaded_data)  # Output: {'key': 'value'}

