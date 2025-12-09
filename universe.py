from classes import Room
import art

world = {
    'start': Room(
        "Castle Gates",
        "You stand before the looming Castle Riccar. The wind howls.",
        "[ VISUAL: A massive iron gate stands shut. "
        "To the west, a dead tree leads to a forest. ]",
        art.castle
    ),
    'forest': Room(
        "Dark Forest",
        "The trees are thick here. Light barely penetrates.",
        "[ VISUAL: Twisted roots have destroyed the northern castle wall here "
        "A glowing moth flutters nearby. ]",
        art.forest
    ),
    'hallway': Room(
        "Grand Hallway",
        "The interior of the castle is cold and dusty.",
        "[ VISUAL: A long red carpet. "
        "A cracked painting hangs on the wall. ]",
        art.painting
    )
}

# Link the rooms (Simple Navigation)
world['start'].add_exit('west', 'forest')
world['forest'].add_exit('east', 'start')
world['forest'].add_exit('north', 'hallway')
world['hallway'].add_exit('south', 'forest')
