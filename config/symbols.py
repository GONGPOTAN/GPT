# config/symbols.py

import json
import os

def get_all_symbols():
    path = os.path.join("config", "symbols.json")
    with open(path, "r") as f:
        return json.load(f)