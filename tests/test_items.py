"""
tests/test_items.py
"""

import sys, os, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from items import spawn_items, use_item, Item, ITEM_TEMPLATES
from entities import Player


class TestItems(unittest.TestCase):

    def test_spawn_items_skips_start_room(self):
        rooms = [(0, 0, 5, 5), (10, 10, 5, 5), (20, 20, 5, 5)]
        items = spawn_items(rooms, count=10)
        start_room = rooms[0]
        for item in items:
            in_start_room = (start_room[0] <= item.x < start_room[0] + start_room[2] and
                              start_room[1] <= item.y < start_room[1] + start_room[3])
            self.assertFalse(in_start_room)

    def test_spawn_items_returns_requested_count(self):
        rooms = [(0, 0, 5, 5), (10, 10, 5, 5)]
        items = spawn_items(rooms, count=4)
        self.assertEqual(len(items), 4)

    def test_potion_heals_player(self):
        player = Player(0, 0)
        player.hp = 5
        potion = Item(0, 0, ITEM_TEMPLATES[0])  # Health Potion, value 8

        use_item(player, potion)

        self.assertEqual(player.hp, min(player.max_hp, 5 + 8))

    def test_weapon_increases_attack_range(self):
        player = Player(0, 0)
        original_range = player.attack_range
        weapon = Item(0, 0, ITEM_TEMPLATES[1])  # Iron Sword, value 2

        use_item(player, weapon)

        self.assertEqual(player.attack_range, (original_range[0] + 2, original_range[1] + 2))

    def test_armor_increases_defense(self):
        player = Player(0, 0)
        original_defense = player.defense
        armor = Item(0, 0, ITEM_TEMPLATES[2])  # Leather Armor, value 1

        use_item(player, armor)

        self.assertEqual(player.defense, original_defense + 1)


if __name__ == "__main__":
    unittest.main()
