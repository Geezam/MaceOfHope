import classes
import enemies
import items
import random
import copy


def spawn_low_level_enemy() -> classes.Enemy:
    """
    Creates a new, battle-ready low-level enemy with unique, random loot.
    """
    enemy_template = random.choice(enemies.low_lvl_ene)
    # CRITICAL: Create a deep copy of the template.
    spawned_enemy = copy.deepcopy(enemy_template)

    loot_to_add = []

    # 50% chance to get an item from the main 'treasure' list
    if random.randint(1, 100) <= 50:
        loot_to_add.append(random.choice(items.treasure))

    unique_items_db = {}
    for item in loot_to_add:
        # handling duplicates
        unique_items_db[item.id] = item

    spawned_enemy.loot = list(unique_items_db.values())

    return spawned_enemy


def spawn_mid_level_enemy() -> classes.Enemy:
    """
    Creates a new, battle-ready mid-level enemy with unique, random loot.
    """
    enemy_template = random.choice(enemies.mid_lvl_ene)
    spawned_enemy = copy.deepcopy(enemy_template)

    loot_to_add = []

    # 100% chance for one treasure
    loot_to_add.append(random.choice(items.treasure))

    # 25% chance for a *second* treasure
    if random.randint(1, 100) <= 25:
        loot_to_add.append(random.choice(items.treasure))

    # handling duplicates
    unique_items_db = {}
    for item in loot_to_add:
        unique_items_db[item.id] = item

    spawned_enemy.loot = list(unique_items_db.values())

    return spawned_enemy
