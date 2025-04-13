# config/symbols.py

import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "symbols.json")

def get_all_symbols():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)