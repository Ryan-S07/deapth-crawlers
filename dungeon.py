"""
dungeon.py

Procedural dungeon generation using Binary Space Partitioning (BSP).

The idea: start with one big rectangle (the whole map). Split it into
two smaller rectangles, either vertically or horizontally. Keep
splitting each piece recursively until the pieces are small enough to
be a room. Carve an actual room inside each leaf piece, then connect
rooms between sibling leaves with an L-shaped corridor.

This is the part of the project that isn't just CRUD/parsing - the
map genuinely comes out different every run.
"""

import random
from constants import MAP_WIDTH, MAP_HEIGHT, MIN_LEAF_SIZE, MAX_LEAF_SIZE, MIN_ROOM_SIZE, WALL, FLOOR


class Leaf:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None
        self.right = None
        self.room = None  # (x, y, w, h) once carved

    def is_leaf(self):
        return self.left is None and self.right is None

    def split(self):
        if not self.is_leaf():
            return False

        # decide split direction: whichever dimension is more "too big"
        split_horizontal = random.random() > 0.5
        if self.width > self.height and self.width / self.height >= 1.25:
            split_horizontal = False
        elif self.height > self.width and self.height / self.width >= 1.25:
            split_horizontal = True

        max_size = self.height if split_horizontal else self.width
        if max_size < MIN_LEAF_SIZE * 2:
            return False  # too small to split further

        split_point = random.randint(MIN_LEAF_SIZE, max_size - MIN_LEAF_SIZE)

        if split_horizontal:
            self.left = Leaf(self.x, self.y, self.width, split_point)
            self.right = Leaf(self.x, self.y + split_point, self.width, self.height - split_point)
        else:
            self.left = Leaf(self.x, self.y, split_point, self.height)
            self.right = Leaf(self.x + split_point, self.y, self.width - split_point, self.height)

        return True

    def get_room(self):
        """Return this leaf's own room, or one from a child if it has no room itself."""
        if self.room:
            return self.room
        left_room = self.left.get_room() if self.left else None
        right_room = self.right.get_room() if self.right else None
        if left_room and right_room:
            return random.choice([left_room, right_room])
        return left_room or right_room


def _build_tree(leaf, depth=0):
    if depth > 8:
        return
    if leaf.split():
        _build_tree(leaf.left, depth + 1)
        _build_tree(leaf.right, depth + 1)


def _carve_room(leaf, grid, rooms):
    if not leaf.is_leaf():
        if leaf.left:
            _carve_room(leaf.left, grid, rooms)
        if leaf.right:
            _carve_room(leaf.right, grid, rooms)
        return

    room_w = random.randint(MIN_ROOM_SIZE, max(MIN_ROOM_SIZE, leaf.width - 2))
    room_h = random.randint(MIN_ROOM_SIZE, max(MIN_ROOM_SIZE, leaf.height - 2))
    room_x = leaf.x + random.randint(1, max(1, leaf.width - room_w - 1))
    room_y = leaf.y + random.randint(1, max(1, leaf.height - room_h - 1))

    room_w = min(room_w, leaf.x + leaf.width - room_x - 1)
    room_h = min(room_h, leaf.y + leaf.height - room_y - 1)

    for y in range(room_y, room_y + room_h):
        for x in range(room_x, room_x + room_w):
            grid[y][x] = FLOOR

    leaf.room = (room_x, room_y, room_w, room_h)
    rooms.append(leaf.room)


def _carve_corridor(grid, x1, y1, x2, y2):
    if random.random() > 0.5:
        _carve_h(grid, x1, x2, y1)
        _carve_v(grid, y1, y2, x2)
    else:
        _carve_v(grid, y1, y2, x1)
        _carve_h(grid, x1, x2, y2)


def _carve_h(grid, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        grid[y][x] = FLOOR


def _carve_v(grid, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        grid[y][x] = FLOOR


def _connect_rooms(leaf, grid):
    if leaf.is_leaf():
        return
    if leaf.left:
        _connect_rooms(leaf.left, grid)
    if leaf.right:
        _connect_rooms(leaf.right, grid)

    if leaf.left and leaf.right:
        room_a = leaf.left.get_room()
        room_b = leaf.right.get_room()
        if room_a and room_b:
            ax = room_a[0] + room_a[2] // 2
            ay = room_a[1] + room_a[3] // 2
            bx = room_b[0] + room_b[2] // 2
            by = room_b[1] + room_b[3] // 2
            _carve_corridor(grid, ax, ay, bx, by)


def generate_dungeon(width=MAP_WIDTH, height=MAP_HEIGHT):
    """Returns (grid, rooms) - grid is a list of lists of WALL/FLOOR, rooms is a list of (x, y, w, h)."""
    grid = [[WALL for _ in range(width)] for _ in range(height)]
    root = Leaf(0, 0, width, height)
    _build_tree(root)

    rooms = []
    _carve_room(root, grid, rooms)
    _connect_rooms(root, grid)

    return grid, rooms


def room_center(room):
    x, y, w, h = room
    return x + w // 2, y + h // 2


def is_walkable(grid, x, y):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == FLOOR


def tile_at(grid, x, y):
    """Safe tile lookup - returns None for out-of-bounds instead of letting
    Python's negative-index wraparound silently read the wrong row/column."""
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return None
    return grid[y][x]
