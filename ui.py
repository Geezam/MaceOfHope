from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console(width=40)


def print_panel(content: Text, title: str, color: str = "green"):
    """
    A general-purpose function to print a rich Panel.
    It takes the content, title, and border color.
    """
    console.print(
        Panel(
            content,
            title=f"--- {title} ---",
            title_align="left",
            border_style=color,
            padding=(1, 2)
        )
    )


def show_hero_profile(hero):
    """
    Gathers hero-specific data and passes it to print_panel.
    """
    profile_text = Text.assemble(
        ("Name:      ", "dim"), (f"{hero.name}\n",
                                 "bold white"),
        ("Class:     ", "dim"), (f"{hero.proff}\n",
                                 "bold white"),
        ("Level:     ", "dim"), (f"{hero.lvl} (XP: {hero.xp}/{hero.lvlNxt})\n",
                                 "white"),
        ("Gold:      ", "dim"), (f"{hero.gold}\n",
                                 "bold yellow"),
        ("\n",),  # Space
        ("HP:        ", "dim"), (f"{hero.sStats['Health']} / {hero.hpMax}\n",
                                 "bold red"),
        ("Attack:    ", "dim"), (f"{hero.atk}\n", "bold"),
        ("Defence:   ", "dim"), (f"{hero.dfn}\n", "bold"),
        ("Speed:     ", "dim"), (f"{hero.speed}\n", "bold"),
        ("Evasion:   ", "dim"), (f"{hero.evasion}%\n", "bold"),
        ("\n",),  # Space
        ("Weapon:    ", "dim"), (f"{hero.equipment['weapon']}\n", "cyan"),
        ("Armour:    ", "dim"), (f"{hero.equipment['armour']}\n", "cyan"),
        ("Accessory: ", "dim"), (f"{hero.equipment['accessory']}\n", "cyan")
    )
    title = f"{hero.name}'s Profile"

    print_panel(profile_text, title, color="green")


def show_enemy_stats(enemy):
    """
    Gathers enemy-specific data and passes it to print_panel.
    """
    stats_text = Text.assemble(
        ("Level:     ", "dim"), (f"{enemy.lvl}\n", "white"),
        ("HP:        ", "dim"), (f"{enemy.sStats['Health']}\n", "bold red"),
        ("Attack:    ", "dim"), (f"{enemy.atk}\n", "bold"),
        ("Defence:   ", "dim"), (f"{enemy.dfn}\n", "bold"),
        ("Speed:     ", "dim"), (f"{enemy.sStats['Speed']}\n", "bold"),
        ("Evasion:   ", "dim"), (f"{enemy.sStats['Evasion']}%\n", "bold"),
        ("\n",),  # Space
        ("XP Reward: ", "dim"), (f"{enemy.xpG}\n", "white"),
        ("Gold Drop: ", "dim"), (f"0 - {enemy.goldG}\n", "yellow")
    )

    stats_text.append("\n",)  # Space
    stats_text.append("Potential Loot:\n", "bold")

    if not enemy.loot:
        stats_text.append("  (None)\n", "dim")
    else:
        for item in enemy.loot:
            stats_text.append(f"  - {item.name}\n", "white")

    title = f"{enemy.name} Stats"

    print_panel(stats_text, title, color="red")


def show_item_stats(item):
    """
    Gathers item-specific data and passes it to print_panel.
    """
    stats_text = Text("")
    if item.hp:
        stats_text.append(f"  HP: {item.hp}\n", style="red")
    if item.atk != [0, 0]:
        stats_text.append(f"  ATK: {item.atk}\n", style="white")
    if item.dfn:
        stats_text.append(f"  DEF: {item.dfn}\n", style="white")
    if item.spd:
        stats_text.append(f"  SPD: {item.spd}\n", style="white")
    if item.eva:
        stats_text.append(f"  EVA: {item.eva}%\n", style="white")

    if not stats_text:
        stats_text = Text("  (No Stats)\n", style="dim")

    full_text = Text.assemble(
        ("Type:  ", "dim"), (f"{item.type.capitalize()}\n", "bold white"),
        ("Value: ", "dim"), (f"{item.value} Gold\n", "yellow"),
        ("\n",),
        ("Stats:\n", "dim"),
        stats_text
    )

    print_panel(full_text, title=item.name, color="blue")


def show_inventory(hero):
    """
    Displays the hero's gold and a list of "treasure" items in their satchel.
    It ignores weapons, armor, and accessories.
    """
    content_text = Text.assemble(
        ("Gold: ", "dim"), (f"{hero.gold}\n\n", "bold yellow"),
        ("Treasures:\n", "bold")
    )

    # Filter the inventory to get *only* treasures
    treasure_items = [item for item in hero.inventory if
                      item.type == "Treasure"]

    # Add treasures to the Text object
    if not treasure_items:
        content_text.append("  (Empty)\n", style="dim")
    else:
        for item in treasure_items:
            content_text.append(f"  - {item.name} ", style="white")
            content_text.append(f"(Value: {item.value}g)\n",
                                style="dim yellow")

    console.print(
        Panel(
            content_text,
            title=f"--- {hero.name}'s Satchel ---",
            title_align="left",
            border_style="yellow",
            padding=(1, 2)
        )
    )
