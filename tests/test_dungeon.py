"""
tests/test_dungeon.py

Checks that dungeon generation produces a valid, connected layout.
"""

import sys, os, unittest
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dungeon import generate_dungeon, is_walkable, room_center, tile_at


def flood_fill_count(grid, start_x, start_y):
    """Count how many floor tiles are reachable from (start_x, start_y)."""
    seen = set()
    queue = deque([(start_x, start_y)])
    seen.add((start_x, start_y))

    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in seen and is_walkable(grid, nx, ny):
                seen.add((nx, ny))
                queue.append((nx, ny))

    return len(seen)


class TestDungeon(unittest.TestCase):

    def test_generates_at_least_one_room(self):
        _, rooms = generate_dungeon()
        self.assertGreaterEqual(len(rooms), 1)

    def test_grid_has_correct_dimensions(self):
        grid, _ = generate_dungeon(width=40, height=16)
        self.assertEqual(len(grid), 16)
        self.assertEqual(len(grid[0]), 40)

    def test_all_rooms_are_reachable(self):
        # run several times since generation is randomized
        for _ in range(5):
            grid, rooms = generate_dungeon()
            start_x, start_y = room_center(rooms[0])
            reachable = flood_fill_count(grid, start_x, start_y)

            total_floor = sum(row.count(".") for row in grid)
            self.assertEqual(reachable, total_floor, "Some floor tiles are not reachable from the start room")

    def test_room_centers_are_walkable(self):
        grid, rooms = generate_dungeon()
        for room in rooms:
            x, y = room_center(room)
            self.assertTrue(is_walkable(grid, x, y))

    def test_tile_at_returns_none_out_of_bounds(self):
        # regression test: Python's negative-index wraparound (grid[-1] silently
        # reading the last row) previously let the player "move" through the
        # top/left edge of the map. tile_at() must return None instead.
        grid, _ = generate_dungeon()
        self.assertIsNone(tile_at(grid, 0, -1))
        self.assertIsNone(tile_at(grid, -1, 0))
        self.assertIsNone(tile_at(grid, 0, len(grid)))
        self.assertIsNone(tile_at(grid, len(grid[0]), 0))


if __name__ == "__main__":
    unittest.main()
