import os
import json
from collections import deque
from providers.ransomlook.config import CACHE_DIR


class RansomLookState:
    
    def __init__(self, cache_dir=CACHE_DIR, filename="state.json", max_items=101):
        self.cache_dir = cache_dir
        self.filename = filename
        self.filepath = os.path.join(self.cache_dir, self.filename)
        self.max_items = max_items
        self.seen_ids = deque(maxlen=self.max_items)  # auto-trim
        os.makedirs(self.cache_dir, exist_ok=True)
        self.load()


    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    ids = data.get("seen_ids", [])
                    # Trim loaded ids if file contains more than max_items
                    self.seen_ids = deque(ids[-self.max_items:], maxlen=self.max_items)
            except Exception as e:
                print(f"[WARN] Error loading state: {e}")


    def save(self):
        try:
            # Only save the last max_items ids
            with open(self.filepath, "w") as f:
                json.dump({"seen_ids": list(self.seen_ids)}, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Unable to save state: {e}")


    def is_new(self, post_id):
        if post_id not in self.seen_ids:
            self.seen_ids.append(post_id)
            return True
        return False
