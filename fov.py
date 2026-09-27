"""
fov.py

Fog of war: a boolean grid the same size as the map, tracking which
tiles the player has already seen. Only those tiles get drawn -
everything else stays blank, even though the actual dungeon layout
is fully generated in memory from the start.

Visibility is just a distance check from the player's position -
not true line-of-sight (walls don't block it), which keeps this
simple enough to reason about and test.
"""

import math
from constants import VISIBILITY_RADIUS


def new_visibility_grid(width, height):
    return [[False for _ in range(width)] for _ in range(height)]


def reveal_around(visibility, px, py, radius=VISIBILITY_RADIUS):
    height = len(visibility)
    width = len(visibility[0])

    for y in range(max(0, py - radius), min(height, py + radius + 1)):
        for x in range(max(0, px - radius), min(width, px + radius + 1)):
            distance = math.sqrt((x - px) ** 2 + (y - py) ** 2)
            if distance <= radius:
                visibility[y][x] = True


def is_visible(visibility, x, y):
    if y < 0 or y >= len(visibility) or x < 0 or x >= len(visibility[0]):
        return False
    return visibility[y][x]
