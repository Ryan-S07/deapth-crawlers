"""
entities.py

Player and Monster classes. Kept intentionally simple - both are
basically a bag of stats plus a couple of helper methods, since the
actual combat math lives in combat.py.
"""

from constants import PLAYER_START_HP, PLAYER_ATTACK_RANGE, PLAYER_DEFENSE


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = PLAYER_START_HP
        self.max_hp = PLAYER_START_HP
        self.attack_range = PLAYER_ATTACK_RANGE
        self.defense = PLAYER_DEFENSE
        self.inventory = []
        self.kills = 0

    def is_alive(self):
        return self.hp > 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)


# base stats per monster type - actual spawned monster stats scale with dungeon depth
MONSTER_TYPES = [
    {"name": "Rat", "symbol": "r", "hp": 6, "attack_range": (1, 3), "defense": 0, "xp": 2},
    {"name": "Goblin", "symbol": "g", "hp": 10, "attack_range": (2, 4), "defense": 1, "xp": 4},
    {"name": "Skeleton", "symbol": "s", "hp": 14, "attack_range": (3, 6), "defense": 2, "xp": 6},
    {"name": "Ogre", "symbol": "O", "hp": 22, "attack_range": (4, 8), "defense": 3, "xp": 10},
]


class Monster:
    def __init__(self, x, y, monster_type, level):
        self.x = x
        self.y = y
        self.name = monster_type["name"]
        self.symbol = monster_type["symbol"]

        level_multiplier = 1 + (level - 1) * 0.15
        self.hp = round(monster_type["hp"] * level_multiplier)
        self.max_hp = self.hp
        lo, hi = monster_type["attack_range"]
        self.attack_range = (round(lo * level_multiplier), round(hi * level_multiplier))
        self.defense = monster_type["defense"]
        self.xp = monster_type["xp"]

    def is_alive(self):
        return self.hp > 0


def spawn_monster(x, y, level):
    monster_type = random_monster_type(level)
    return Monster(x, y, monster_type, level)


def random_monster_type(level):
    import random
    # deeper levels bias towards the tougher monster types
    weights = []
    for i, m in enumerate(MONSTER_TYPES):
        weight = max(1, 5 - abs(i - min(level - 1, len(MONSTER_TYPES) - 1)) * 2)
        weights.append(weight)
    return random.choices(MONSTER_TYPES, weights=weights, k=1)[0]
