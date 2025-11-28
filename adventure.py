import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import ui
import functions
import spawn
import classes

console = Console()


class Room:
    def __init__(self, name, description, image_desc):
        self.name = name
        self.description = description
        self.image_desc = image_desc
        self.exits = {}      # {'north': 'Room_ID'}
        self.encounter_rate = 0.2  # 20% chance of battle

    def add_exit(self, direction, room_key):
        self.exits[direction] = room_key


world = {
    'start': Room(
        "Castle Gates",
        "You stand before the looming Castle Riccar. The wind howls.",
        "[ VISUAL: A massive iron gate stands shut. "
        "To the side, a dead tree. ]"
    ),
    'forest': Room(
        "Dark Forest",
        "The trees are thick here. Light barely penetrates.",
        "[ VISUAL: Twisted roots cover the path. "
        "A glowing moth flutters nearby. ]"
    ),
    'hallway': Room(
        "Grand Hallway",
        "The interior of the castle is cold and dusty.",
        "[ VISUAL: A long red carpet. "
        "A cracked painting hangs on the wall. ]"
    )
}

# Link the rooms (Simple Navigation)
world['start'].add_exit('north', 'forest')
world['forest'].add_exit('south', 'start')
world['forest'].add_exit('enter', 'hallway')
world['hallway'].add_exit('exit', 'forest')


def render_screen(hero, room):
    """Displays the Room Visuals and Hero Status"""
    console.clear()

    # Top Panel: Room View
    view_content = (f"[bold yellow]{room.name}[/bold yellow]\n\n"
                    f"{room.image_desc}\n\n"
                    f"[italic]{room.description}[/italic]")
    console.print(Panel(view_content, title="Current Location", style="cyan"))

    # Bottom Panel: Hero Status
    current_hp = hero.sStats['Health']
    status_text = (f"HP: {current_hp}/{hero.hpMax} | Lvl: {hero.lvl} | "
                   f"XP: {hero.xp} | Gold: {hero.gold}")
    console.print(Panel(status_text, style="green"))


def trigger_random_encounter(player):
    """Handles random battles with spawn logic"""
    console.print("[bold red]!! A MONSTER AMBUSHES YOU !![/bold red]")

    if player.lvl < 3:
        foe = spawn.spawn_low_level_enemy()
    else:
        foe = spawn.spawn_mid_level_enemy()

    functions.commands(player, foe)

    if player.sStats['Health'] > 0:
        Prompt.ask("[bold]Battle complete. Press Enter to continue...[/bold]")


# MAIN GAME LOOP
def main():
    # Setup Hero
    player = classes.Hero(
        name="Geezam",
        proff="Ranger",
        affin="Gray",
        pstats=(5, 3, 2)
    )

    # Create & Equip Items
    ring = classes.Item(id=1, name="Ruby Ring", type="accessory",
                        atk=[1, 1], hp=9)
    sword = classes.Item(id=2, name="Rusty Peg", type="weapon",
                         atk=[2, 5])
    vest = classes.Item(id=3, name="Iron Vest", type="armour",
                        dfn=9)

    functions.equip_item(player, ring)
    functions.equip_item(player, sword)
    functions.equip_item(player, vest)

    # Show initial profile
    console.print("[bold]Initializing Game...[/bold]")
    player.profile()
    Prompt.ask("Press Enter to start your adventure...")

    # Navigation Start
    current_room_key = 'start'

    while True:
        # 1. Check if dead
        if player.sStats["Health"] <= 0:
            console.print("[bold red]You have been defeated. "
                          "Game Over.[/bold red]")
            break

        # 2. Render World
        room = world[current_room_key]
        render_screen(player, room)

        # 3. Get Input
        console.print("[bold]Commands:[/bold] [N]orth, [S]outh, [E]ast, [W]est"
                      ", [Enter], [I]nventory, [P]rofile, [Q]uit")
        action = Prompt.ask("What do you do?").lower().strip()

        if action == "":
            continue

        # 4. Handle Actions
        direction = None

        # Movement Mapping
        if action in ['n', 'north']:
            direction = 'north'
        elif action in ['s', 'south']:
            direction = 'south'
        elif action in ['e', 'east']:
            direction = 'east'
        elif action in ['w', 'west']:
            direction = 'west'
        elif action in ['enter']:
            direction = 'enter'
        elif action in ['exit']:
            direction = 'exit'

        # Other Commands
        elif action in ['i', 'inventory']:
            ui.show_inventory(player)
            Prompt.ask("Press Enter to return...")
            continue
        elif action in ['p', 'profile']:
            player.profile()
            Prompt.ask("Press Enter to return...")
            continue
        elif action in ['q', 'quit']:
            console.print("Thanks for playing!")
            break
        else:
            console.print("[italic red]Invalid command.[/italic red]")
            continue

        # 5. Execute Movement
        if direction:
            if direction in room.exits:
                # A. Random Battle Check
                if random.random() < room.encounter_rate:
                    trigger_random_encounter(player)
                    # If player died in battle, loop will catch it at top
                    if player.sStats["Health"] <= 0:
                        continue

                # B. Move
                current_room_key = room.exits[direction]
            else:
                console.print("[italic]You can't go that way.[/italic]")
                Prompt.ask("Press Enter...")


if __name__ == "__main__":
    main()
