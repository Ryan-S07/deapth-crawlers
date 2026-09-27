"""
constants.py

All the fixed numbers and symbols used across the game, kept in one
place so tuning the game (map size, difficulty, etc.) doesn't mean
hunting through every file.
"""

MAP_WIDTH = 60
MAP_HEIGHT = 14

MIN_LEAF_SIZE = 10
MAX_LEAF_SIZE = 24
MIN_ROOM_SIZE = 4

WALL = "█"
FLOOR = "."
STAIRS_DOWN = ">"
UNKNOWN = " "

LEGEND = [
    ("@", "You"),
    (WALL, "Wall"),
    (".", "Floor"),
    (">", "Stairs"),
    ("!", "Potion"),
    ("/", "Weapon"),
    ("[", "Armor"),
    ("letters", "Monster"),
]

VISIBILITY_RADIUS = 5

PLAYER_START_HP = 20
PLAYER_ATTACK_RANGE = (2, 5)
PLAYER_DEFENSE = 1

ITEMS_PER_LEVEL = 3
MONSTERS_PER_LEVEL = 4

SAVE_FILE = "data/highscores.json"
