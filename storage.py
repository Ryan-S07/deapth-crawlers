"""
storage.py

Saves a short summary of each run (depth reached, kills, turns taken)
to a JSON file so there's a persistent high score list between games.
"""

import json
import os
from constants import SAVE_FILE


def load_runs(path=SAVE_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_run(level, kills, turns, path=SAVE_FILE):
    runs = load_runs(path)
    runs.append({"level": level, "kills": kills, "turns": turns})
    runs.sort(key=lambda r: (r["level"], r["kills"]), reverse=True)
    runs = runs[:10]  # keep top 10

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(runs, f, indent=2)

    return runs
