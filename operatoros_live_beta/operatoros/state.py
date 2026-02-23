import json
import os

class State:
    def __init__(self, filename):
        self.filename = filename
        self.data = {
            "day": 1,
            "history": [],
            "current_niche": None,
            "daily_limit": 1,
            "autopick": False
        }

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.data.update(json.load(f))

    def save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
