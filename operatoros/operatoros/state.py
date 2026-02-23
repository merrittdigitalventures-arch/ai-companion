import json
import os

def load_state(file_path="data/state.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_state(file_path="data/state.json", state=None):
    if state is None:
        state = {}
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(state, f, indent=4)

def advance_day(state):
    state["day"] = state.get("day", 1) + 1
