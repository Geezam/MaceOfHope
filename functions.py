import classes
import ui
from random import randint
from typing import Union

# Define a type for combatants
Combatant = Union[classes.Hero, classes.Enemy]


def fight(atker: Combatant, dfnder: Combatant):
    """
    Handles a single attack from atker to dfnder,
    checking for evasion and defense.
    """
    evasion_roll = randint(1, 100)
    if isinstance(dfnder, classes.Hero):
        defender_evasion_chance = dfnder.evasion
    else:
        defender_evasion_chance = dfnder.sStats["Evasion"]

    if evasion_roll <= defender_evasion_chance:
        print(f"{atker.name} attacks, but {dfnder.name} dodges the blow!")
        return

    attack_roll = randint(atker.atk[0], atker.atk[1])

    defender_defense = dfnder.dfn

    if attack_roll >= defender_defense:
        damage_dealt = attack_roll - defender_defense
        # possible to hit but roll zero damage depending on weapon/debuffs
        if damage_dealt <= 0:
            print(f"{atker.name}'s attack hits but does no damage to "
                  f"{dfnder.name}'s health!")
            return
        else:

            print(f"{atker.name}'s attack ({attack_roll}) breaks through "
                  f"{dfnder.name}'s defense ({defender_defense})!")

    else:
        # The attack hit but was not strong enough.
        print(f"{atker.name}'s attack ({attack_roll}) is blocked "
              f"by {dfnder.name}'s defense ({defender_defense})!")
        return

    dfnder_hp = dfnder.sStats["Health"]
    dfnder_hp -= damage_dealt
    dfnder.sStats["Health"] = dfnder_hp

    if dfnder_hp <= 0:
        dfnder.sStats["Health"] = 0  # Ensure HP doesn't show as negative
        print(f"{dfnder.name} takes {damage_dealt} damage and has been slain!")

        # Check if the attacker is the Hero to give XP
        if isinstance(atker, classes.Hero):
            print(f"{atker.name} gained {dfnder.xpG} XP!")
            gold_found = randint(0, dfnder.goldG)
            atker.gold += gold_found
            print(f"{atker.name} found {gold_found} gold!\n")

            if dfnder.loot:
                print(f"{dfnder.name} dropped:")
                for item in dfnder.loot:
                    print(f"  > {item.name}")
                    atker.inventory.append(item)
                print("")

            lvler(atker, dfnder.xpG)
            atker.profile()
        else:
            # The defender must be the Hero
            print(f"GAME OVER: {dfnder.name} has fallen.")
            print(f"{atker.name} devours {dfnder.name}'s lifeless corpse.")
    else:
        # The defender survives
        print(f"{dfnder.name} takes {damage_dealt} damage! ({dfnder_hp} "
              f"HP remaining)")


def commands(fghter1: classes.Hero, fghter2: classes.Enemy):
    """
    Main battle loop.
    Decides turn order based on Speed.
    """
    round_num = 2
    print(f"\nA wild {fghter2.name} appears!")
    ui.show_enemy_stats(fghter2)

    player_speed = fghter1.speed
    enemy_speed = fghter2.sStats["Speed"]

    if player_speed == enemy_speed:
        print("Both combatants have the same speed!")
        if randint(0, 1) == 0:
            first_attacker = fghter1
            second_attacker = fghter2
            print("Player wins the coin toss and attacks first!")
        else:
            first_attacker = fghter2
            second_attacker = fghter1
            print("Enemy wins the coin toss and attacks first!")

    elif player_speed > enemy_speed:
        first_attacker = fghter1
        second_attacker = fghter2
        print(f"{fghter1.name} is faster and attacks first!")

    else:
        first_attacker = fghter2
        second_attacker = fghter1
        print(f"{fghter2.name} is faster and attacks first!")

    fight(first_attacker, second_attacker)

    # Calculate the percentage chance for the player to attack.
    total_speed = player_speed + enemy_speed

    # Ensure total_speed is not zero to avoid ZeroDivisionError
    if total_speed == 0:
        player_attack_chance = 50
    else:
        player_attack_chance = (player_speed / total_speed) * 100
    if player_speed > enemy_speed:
        print(f"({fghter1.name} is faster than {fghter2.name}: "
              f"attack chance per round: {player_attack_chance:.0f}%)")
    elif enemy_speed > player_speed:
        print(f"({fghter2.name} is faster than {fghter1.name}: "
              f"attack chance per round: {player_attack_chance:.0f}%)")
    else:
        print("Both combatants have the same speed!")

    # The loop continues as long as both are alive
    while fghter1.sStats["Health"] > 0 and fghter2.sStats["Health"] > 0:

        input(f"\nPress Enter to continue to Round {round_num}...")
        round_num += 1

        # Probability Turn Roll
        turn_roll = randint(1, 100)

        if turn_roll <= player_attack_chance:
            # Player's turn to attack
            print(f"\n--- {fghter1.name}'s Turn ---")
            fight(fghter1, fghter2)
        else:
            # Enemy's turn to attack
            print(f"\n--- {fghter2.name}'s Turn ---")
            fight(fghter2, fghter1)

    if fghter1.sStats["Health"] > 0 and fghter2.sStats["Health"] <= 0:
        print(f"\n{fghter1.name} is victorious!")
    elif fghter1.sStats["Health"] <= 0:
        print(f"\n{fghter1.name} has been defeated...")


def lvler(hero: classes.Hero, xp_gain: int):
    """
    Handles adding XP and leveling up the hero.
    """
    total_xp = hero.xp + xp_gain

    if total_xp < hero.lvlNxt:  # Not enough to level
        hero.xp = total_xp
        return

    # --- LEVEL UP! ---
    while total_xp >= hero.lvlNxt:
        hero.lvl += 1  # Raise level

        # Calculate new max HP
        hero.base_hpMax = round(hero.base_hpMax * 1.2)
        # Heal to new max HP
        hero.sStats["Health"] = hero.hpMax

        # Raise other stats
        hero.base_speed = round(hero.base_speed * 1.2)
        hero.base_evasion = round(hero.base_evasion * 1.2)

        # Calculate XP remaining and next level cost
        total_xp -= hero.lvlNxt
        hero.xp = total_xp
        hero.lvlNxt = round(hero.lvlNxt * 1.5)

        print(f"*** DING! {hero.name} reached Level {hero.lvl}! ***")
        print(f"HP is now {hero.hpMax}.")


def equip_item(hero: classes.Hero, item: classes.Item):
    """
    Equips an item to the hero, setting the BASE stats or BONUSES.
    """
    if item.type == "accessory":
        # Unequip old item first
        unequip_item(hero, "accessory")

        print(f"Equipping {item.name}.")
        hero.equipment["accessory"] = item.name
        # Set ALL accessory bonuses
        hero.acc_hp_bonus = item.hp
        hero.acc_spd_bonus = item.spd
        hero.acc_eva_bonus = item.eva
        hero.acc_atk_bonus = item.atk
        hero.acc_dfn_bonus = item.dfn

    elif item.type == "weapon":
        unequip_item(hero, "weapon")
        print(f"Equipping {item.name}.")
        hero.equipment["weapon"] = item.name
        hero.base_atk = item.atk

    elif item.type == "armour":
        unequip_item(hero, "armour")
        print(f"Equipping {item.name}.")
        hero.equipment["armour"] = item.name
        hero.base_dfn = item.dfn

    # After equipping, check if current HP is too high
    if hero.sStats["Health"] > hero.hpMax:
        hero.sStats["Health"] = hero.hpMax


def unequip_item(hero: classes.Hero, slot: str):
    """
    Unequips an item from a slot and resets its bonuses.
    Slot must be "weapon", "armour", or "accessory".
    """
    if slot == "accessory":
        if hero.equipment["accessory"] == "none":
            return

        print(f"Unequipped {hero.equipment['accessory']}.")
        hero.equipment["accessory"] = "none"
        # Reset ALL accessory bonuses
        hero.acc_hp_bonus = 0
        hero.acc_spd_bonus = 0
        hero.acc_eva_bonus = 0
        hero.acc_atk_bonus = [0, 0]
        hero.acc_dfn_bonus = 0

    elif slot == "weapon":
        hero.equipment["weapon"] = "unarmed"
        hero.base_atk = [1, 2]

    elif slot == "armour":
        hero.equipment["armour"] = "nekkid"
        hero.base_dfn = 0

    else:
        return

    # Check HP after unequipping
    if hero.sStats["Health"] > hero.hpMax:
        hero.sStats["Health"] = hero.hpMax
