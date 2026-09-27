"""
tests/test_combat.py
"""

import sys, os, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from combat import roll_damage, resolve_combat_round
from entities import Player, Monster, MONSTER_TYPES


class TestCombat(unittest.TestCase):

    def test_damage_is_never_below_one(self):
        for _ in range(100):
            dmg = roll_damage((1, 2), defense=999)
            self.assertGreaterEqual(dmg, 1)

    def test_damage_within_expected_range_before_defense(self):
        for _ in range(100):
            dmg = roll_damage((3, 6), defense=0)
            self.assertTrue(3 <= dmg <= 6)

    def test_combat_round_can_kill_monster(self):
        player = Player(0, 0)
        player.attack_range = (999, 999)  # guarantee a one-hit kill for this test
        monster = Monster(0, 0, MONSTER_TYPES[0], level=1)

        log = resolve_combat_round(player, monster)

        self.assertFalse(monster.is_alive())
        self.assertEqual(player.kills, 1)
        self.assertIn("dies", log[-1])

    def test_combat_round_can_kill_player(self):
        player = Player(0, 0)
        player.hp = 1
        player.attack_range = (0, 0)  # won't actually kill the monster this round
        monster = Monster(0, 0, MONSTER_TYPES[3], level=5)  # tough monster

        resolve_combat_round(player, monster)

        self.assertFalse(player.is_alive())


if __name__ == "__main__":
    unittest.main()
