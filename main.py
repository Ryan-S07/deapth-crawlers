"""
main.py

Entry point. Run with: python3 main.py

Ties every module together into the actual game loop: generate a
level, let the player move/fight/loot, descend on stairs, end the
run on death.
"""

import curses
import locale
import random

from dungeon import generate_dungeon, room_center, tile_at
from entities import Player, spawn_monster
from items import spawn_items, use_item
from combat import resolve_combat_round
from fov import new_visibility_grid, reveal_around
from render import draw_dungeon, draw_game_over, draw_inventory_screen, terminal_too_small, draw_too_small_message
from storage import save_run
from constants import MONSTERS_PER_LEVEL, ITEMS_PER_LEVEL, STAIRS_DOWN, FLOOR, MAP_WIDTH, MAP_HEIGHT


def build_level(level):
    grid, rooms = generate_dungeon()

    start_x, start_y = room_center(rooms[0])

    stairs_room = rooms[-1] if len(rooms) > 1 else rooms[0]
    stairs_x, stairs_y = room_center(stairs_room)
    grid[stairs_y][stairs_x] = STAIRS_DOWN

    monsters = []
    for _ in range(MONSTERS_PER_LEVEL):
        room = random.choice(rooms[1:]) if len(rooms) > 1 else rooms[0]
        mx, my = room_center(room)
        mx = min(max(mx + random.randint(-1, 1), room[0] + 1), room[0] + room[2] - 2)
        my = min(max(my + random.randint(-1, 1), room[1] + 1), room[1] + room[3] - 2)
        monsters.append(spawn_monster(mx, my, level))

    items = spawn_items(rooms, ITEMS_PER_LEVEL)

    return grid, rooms, monsters, items, (start_x, start_y), (stairs_x, stairs_y)


def monster_at(monsters, x, y):
    for m in monsters:
        if m.is_alive() and m.x == x and m.y == y:
            return m
    return None


def item_at(items, x, y):
    for i in items:
        if i.x == x and i.y == y:
            return i
    return None


def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    if terminal_too_small(MAP_WIDTH, MAP_HEIGHT):
        draw_too_small_message(stdscr, MAP_WIDTH, MAP_HEIGHT)
        return

    level = 1
    player = Player(0, 0)
    turns = 0
    message = "Welcome to Depthcrawl. Find the stairs (>) to descend. Press i for controls/legend."

    grid, rooms, monsters, items, start_pos, stairs_pos = build_level(level)
    player.x, player.y = start_pos

    visibility = new_visibility_grid(MAP_WIDTH, MAP_HEIGHT)
    reveal_around(visibility, player.x, player.y)

    while True:
        if terminal_too_small(MAP_WIDTH, MAP_HEIGHT):
            draw_too_small_message(stdscr, MAP_WIDTH, MAP_HEIGHT)
            return

        draw_dungeon(stdscr, grid, visibility, monsters, items, player, level, message)

        curses.flushinp()  # discard any buffered repeat keystrokes before reading
        key = stdscr.getch()

        dx, dy = 0, 0
        if key == curses.KEY_UP:
            dy = -1
        elif key == curses.KEY_DOWN:
            dy = 1
        elif key == curses.KEY_LEFT:
            dx = -1
        elif key == curses.KEY_RIGHT:
            dx = 1
        elif key == ord("q"):
            break
        elif key == ord("i"):
            draw_inventory_screen(stdscr, player)
            continue
        else:
            continue

        new_x, new_y = player.x + dx, player.y + dy

        blocking_monster = monster_at(monsters, new_x, new_y)
        if blocking_monster:
            log = resolve_combat_round(player, blocking_monster)
            message = " ".join(log)
            turns += 1
            if not player.is_alive():
                draw_game_over(stdscr, level, player.kills, turns)
                save_run(level, player.kills, turns)
                return
            continue

        # tile_at() returns None for anything out of bounds instead of letting
        # Python wrap negative indices around to the opposite edge of the grid
        tile = tile_at(grid, new_x, new_y)
        if tile not in (FLOOR, STAIRS_DOWN):
            continue

        player.move(dx, dy)
        turns += 1
        reveal_around(visibility, player.x, player.y)

        picked_up = item_at(items, player.x, player.y)
        if picked_up:
            message = use_item(player, picked_up)
            items.remove(picked_up)
            player.inventory.append(picked_up.name)

        if (player.x, player.y) == stairs_pos:
            level += 1
            grid, rooms, monsters, items, start_pos, stairs_pos = build_level(level)
            player.x, player.y = start_pos
            visibility = new_visibility_grid(MAP_WIDTH, MAP_HEIGHT)
            reveal_around(visibility, player.x, player.y)
            message = f"You descend to level {level}."

    save_run(level, player.kills, turns)


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")  # needed so the block-wall character renders correctly
    curses.wrapper(game_loop)
