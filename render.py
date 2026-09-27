"""
render.py

All the curses drawing code lives here, kept separate from main.py so
the actual game rules don't depend on curses at all (and can be unit
tested without a terminal).

Layout: a bordered map panel on top, a bordered HUD panel (stats,
last message, legend, controls) underneath.

Refresh pattern: every window calls .noutrefresh() (stage the update,
no immediate screen paint), then a single curses.doupdate() flushes
everything together at the end of each draw call. Calling .refresh()
on each window individually - or worse, calling stdscr.refresh() after
already refreshing sub-windows - causes visible flicker, and can wipe
out sub-windows entirely, since stdscr.refresh() repaints the (blank)
base screen on top of whatever the sub-windows just drew.
"""

import curses
from constants import LEGEND

HUD_LINES = 4
HUD_HEIGHT = HUD_LINES + 2


def required_size(map_width, map_height):
    """(width, height) the terminal must be at least, for the full UI to fit."""
    return map_width + 2, map_height + 2 + HUD_HEIGHT


def terminal_too_small(map_width, map_height):
    need_w, need_h = required_size(map_width, map_height)
    return curses.COLS < need_w or curses.LINES < need_h


def draw_too_small_message(stdscr, map_width, map_height):
    need_w, need_h = required_size(map_width, map_height)
    stdscr.erase()
    lines = [
        "Terminal window is too small for Depthcrawl.",
        f"Need at least {need_w} columns x {need_h} rows.",
        f"Current size: {curses.COLS} columns x {curses.LINES} rows.",
        "Resize/maximize your terminal (or reduce font size), then restart.",
        "Press any key to exit.",
    ]
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(i, 0, line)
        except curses.error:
            pass
    stdscr.refresh()
    stdscr.getch()


def draw_dungeon(stdscr, grid, visibility, monsters, items, player, level, message):
    stdscr.erase()
    stdscr.noutrefresh()

    height = len(grid)
    width = len(grid[0])

    map_win = curses.newwin(height + 2, width + 2, 0, 0)
    map_win.box()

    for y in range(height):
        for x in range(width):
            if not visibility[y][x]:
                continue
            _safe_addstr(map_win, y + 1, x + 1, grid[y][x])

    for item in items:
        if visibility[item.y][item.x]:
            _safe_addstr(map_win, item.y + 1, item.x + 1, item.symbol)

    for monster in monsters:
        if monster.is_alive() and visibility[monster.y][monster.x]:
            _safe_addstr(map_win, monster.y + 1, monster.x + 1, monster.symbol)

    _safe_addstr(map_win, player.y + 1, player.x + 1, "@")
    map_win.noutrefresh()

    _draw_hud(width, height, player, level, message)

    curses.doupdate()


def _draw_hud(map_width, map_height, player, level, message):
    hud_lines = [
        f"Level: {level}   HP: {player.hp}/{player.max_hp}   Kills: {player.kills}   Items: {len(player.inventory)}",
        f"{message}",
        "Legend: " + "  ".join(f"{sym}={meaning}" for sym, meaning in LEGEND),
        "Controls: Arrow keys move/attack | i = inventory | q = quit",
    ]

    hud_win = curses.newwin(HUD_HEIGHT, map_width + 2, map_height + 2, 0)
    hud_win.box()

    for row, line in enumerate(hud_lines, start=1):
        _safe_addstr(hud_win, row, 1, line[:map_width])

    hud_win.noutrefresh()


def draw_inventory_screen(stdscr, player):
    """A separate bordered screen listing the player's items. Waits for any
    keypress before returning control to the main game loop (the "back" key)."""
    stdscr.erase()
    stdscr.noutrefresh()

    height, width = 14, 50
    win = curses.newwin(height, width, 1, 1)
    win.box()

    _safe_addstr(win, 1, 2, "Inventory")

    if not player.inventory:
        _safe_addstr(win, 3, 2, "(empty)")
    else:
        for i, item_name in enumerate(player.inventory):
            if i >= height - 5:
                _safe_addstr(win, 3 + i, 2, "...")
                break
            _safe_addstr(win, 3 + i, 2, f"- {item_name}")

    _safe_addstr(win, height - 2, 2, "Press any key to go back")
    win.noutrefresh()
    curses.doupdate()
    stdscr.getch()  # this is the "back" key - any key returns to the game


def draw_game_over(stdscr, level, kills, turns):
    stdscr.erase()
    stdscr.noutrefresh()

    win = curses.newwin(10, 40, 1, 1)
    win.box()
    _safe_addstr(win, 1, 2, "You have died.")
    _safe_addstr(win, 3, 2, f"Level reached: {level}")
    _safe_addstr(win, 4, 2, f"Monsters killed: {kills}")
    _safe_addstr(win, 5, 2, f"Turns taken: {turns}")
    _safe_addstr(win, 7, 2, "Press any key to exit.")
    win.noutrefresh()
    curses.doupdate()
    stdscr.getch()


def _safe_addstr(win, y, x, text):
    try:
        win.addstr(y, x, text)
    except curses.error:
        pass  # writing to the very last cell of a window raises harmlessly
