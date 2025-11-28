import ui
import classes
import functions
import spawn
# Create a hero instance
# Profession (proff) - Warrior/Ranger/Rogue
# Change to Rhyoo - Rock, Peige - Paper, Scher - Scissors LATER
# Primary Stats (pstats) Order - Vitality, Dexterity, Intelligence
# Affinity implimentation for "choices" later - red/gray/green

player = classes.Hero(name="Geezam",
                      proff="Ranger",
                      affin="Gray",
                      pstats=(5, 3, 2))

# show player profile
player.profile()

# Create example items
ring = classes.Item(id=1, name="Ruby Ring", type="accessory", atk=[1, 1], hp=9)
sword = classes.Item(id=2, name="Rusty Peg", type="weapon", atk=[2, 5])
vest = classes.Item(id=3, name="Iron Vest", type="armour", dfn=9)

# Equip items
functions.equip_item(player, ring)
functions.equip_item(player, sword)
functions.equip_item(player, vest)

print("\n--- After equipping ---")
player.profile()

# --- Main Game Loop ---
while True:
    # Check if player is alive
    if player.sStats["Health"] <= 0:
        print("You have been defeated. Game Over.")
        break

    print("\n--- What would you like to do? ---")
    action = input("1 - fight | "
                   "2 - inventory | "
                   "3 - profile | "
                   "4 - quit\n> ").lower()

    if action == "fight" or action == "1":
        # Create an enemy
        if player.lvl < 3:
            print("(Spawning a low-level enemy...)")
            foe = spawn.spawn_low_level_enemy()
        else:
            print("(Spawning a mid-level enemy...)")
            foe = spawn.spawn_mid_level_enemy()

        # Start the fight!
        functions.commands(player, foe)

    elif action == "inventory" or action == "2":
        ui.show_inventory(player)

    elif action == "profile" or action == "3":
        player.profile()

    elif action == "quit" or action == "4":
        print("Thanks for playing!")
        break

    else:
        print("Invalid command.")
