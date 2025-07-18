import json
import os

DATA_FOLDER = "data"

def load_data(filename):
    path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_data(filename, data):
    path = os.path.join(DATA_FOLDER, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
