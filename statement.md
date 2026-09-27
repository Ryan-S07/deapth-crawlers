# Problem Statement

Most beginner-level Python projects (to-do apps, calculators, simple
CRUD tools) don't demonstrate algorithmic thinking beyond basic
control flow and data structures. This project instead builds a
procedurally generated roguelike game, where the core challenge is
genuinely algorithmic: generating a random, fully-connected dungeon
layout every run, rather than reading/writing fixed data.

## Objectives

- Apply Binary Space Partitioning (BSP) to procedurally generate a
  random, fully-connected dungeon layout every run, rather than using
  fixed or hand-designed levels
- Implement a complete turn-based game loop — movement, combat,
  inventory, and progression — entirely in the Python standard
  library, runnable from any terminal
- Demonstrate correct application of core course concepts: recursion,
  2D-grid/list manipulation, OOP (Player/Monster/Item classes),
  randomized algorithms, file I/O, and automated unit testing
- Verify correctness programmatically (e.g. dungeon connectivity via
  flood-fill) rather than relying only on manual/visual inspection

## Scope

Depthcrawl is a terminal-based, turn-based dungeon crawler that:
- Procedurally generates a new dungeon layout every level using
  Binary Space Partitioning (BSP)
- Places the player, monsters, and items into that generated layout,
  with monster difficulty scaling by depth
- Resolves turn-based combat when the player walks into a monster
- Reveals the map progressively through a fog-of-war system as the
  player explores
- Tracks inventory and applies item effects (healing, attack/defense
  boosts)
- Saves a persistent high-score list (depth reached, kills, turns
  taken) between sessions

It does not include real-time movement, networked/multiplayer play,
or graphical rendering — everything runs through the terminal via the
standard library `curses` module.

## Target users

Anyone who wants a quick, replayable terminal game — built here
specifically as a Python Essentials project to demonstrate recursion,
2D-grid manipulation, OOP (Player/Monster/Item classes), randomized
algorithms, file I/O, and unit testing, applied to something more
substantial than a CRUD app.

## High-level features

1. **Procedural dungeon generation** — recursive BSP splitting, room
   carving, and corridor connection between sibling rooms
2. **Turn-based combat** — randomized damage rolls reduced by
   defense, resolved player-then-monster per turn
3. **Fog of war** — distance-based visibility revealed as the player
   moves
4. **Inventory system** — potions/weapons/armor spawned in rooms,
   auto-applied on pickup
5. **Persistence** — JSON-based high-score tracking across runs
