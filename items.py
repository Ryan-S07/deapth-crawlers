"""
items.py

Items are dropped in rooms and picked up by walking onto them.
Three simple types are enough to make choices matter without
overcomplicating the project: potions heal, weapons raise attack,
armor raises defense.
"""

import random

ITEM_TEMPLATES = [
    {"name": "Health Potion", "symbol": "!", "type": "potion", "value": 8},
    {"name": "Iron Sword", "symbol": "/", "type": "weapon", "value": 2},
    {"name": "Leather Armor", "symbol": "[", "type": "armor", "value": 1},
]


class Item:
    def __init__(self, x, y, template):
        self.x = x
        self.y = y
        self.name = template["name"]
        self.symbol = template["symbol"]
        self.type = template["type"]
        self.value = template["value"]


def spawn_items(rooms, count):
    """Place `count` random items in random rooms (never in rooms[0], the start room)."""
    items = []
    if len(rooms) <= 1:
        return items

    for _ in range(count):
        room = random.choice(rooms[1:])
        x = random.randint(room[0] + 1, room[0] + room[2] - 2) if room[2] > 2 else room[0]
        y = random.randint(room[1] + 1, room[1] + room[3] - 2) if room[3] > 2 else room[1]
        template = random.choice(ITEM_TEMPLATES)
        items.append(Item(x, y, template))

    return items


def use_item(player, item):
    """Apply an item's effect to the player. Returns a message string."""
    if item.type == "potion":
        player.heal(item.value)
        return f"You drink the {item.name} and recover {item.value} HP."
    elif item.type == "weapon":
        lo, hi = player.attack_range
        player.attack_range = (lo + item.value, hi + item.value)
        return f"You equip the {item.name}. Attack increased."
    elif item.type == "armor":
        player.defense += item.value
        return f"You equip the {item.name}. Defense increased."
    return f"You can't use the {item.name} right now."
