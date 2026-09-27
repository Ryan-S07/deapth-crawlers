"""
combat.py

Combat is turn-based and resolved with simple randomized damage rolls
minus the defender's defense stat. Kept as plain functions (not
methods on the entities) so it's easy to unit test without needing a
Player and Monster fighting inside a full game loop.
"""

import random


def roll_damage(attack_range, defense):
    lo, hi = attack_range
    raw_damage = random.randint(lo, hi)
    final_damage = max(1, raw_damage - defense)  # every hit does at least 1
    return final_damage


def player_attacks(player, monster):
    damage = roll_damage(player.attack_range, monster.defense)
    monster.hp -= damage
    return damage


def monster_attacks(monster, player):
    damage = roll_damage(monster.attack_range, player.defense)
    player.hp -= damage
    return damage


def resolve_combat_round(player, monster):
    """
    Player attacks first. If the monster survives, it attacks back.
    Returns a list of log message strings describing what happened.
    """
    log = []

    dmg = player_attacks(player, monster)
    log.append(f"You hit the {monster.name} for {dmg} damage.")

    if not monster.is_alive():
        log.append(f"The {monster.name} dies!")
        player.kills += 1
        return log

    dmg = monster_attacks(monster, player)
    log.append(f"The {monster.name} hits you for {dmg} damage.")

    if not player.is_alive():
        log.append("You have died.")

    return log
