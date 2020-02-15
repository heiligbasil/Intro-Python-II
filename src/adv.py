import sys
import textwrap
from room import Room
from player import Player
from item import Item
from colorama import Fore, Back, Style
import colorama

# Initialize the ANSI engine for Windows
colorama.init(autoreset=True)

# Declare all the rooms
room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons."),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together
room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']


# Declare all of the items
item = [Item('torch', 'A dry torch with only the top burnt.'),
        Item('matchbook', 'A full book of dry intact matches.'),
        Item('rope', 'A coiled sturdy-looking dry twisted rope of twine.'),
        Item('dagger', 'A rusting and blunt weapon in a sheath.'), ]


# Link the items to the rooms
room['foyer'].items = [item[0]]
room['overlook'].items = [item[1]]
room['narrow'].items = [item[2]]
room['treasure'].items = [item[3]]


#
# Main
#


# Make a new player object that is currently in the 'outside' room.
player: Player = Player(input("What's your name? ") or 'Kowalksi',
                        room['outside'])
print(f'{Back.WHITE}{Fore.BLACK}Welcome, {player.name} :)')


# REPL command loop - the game's engine
while True:
    print(f'{Fore.BLUE}|<>| Location |<>|')
    print(f"{player.name}'s current location is {Back.MAGENTA}{player.current_room.name}{Back.RESET}.")
    print(textwrap.TextWrapper(width=65).fill(player.current_room.description))
    if len(player.current_room.items) > 0:
        for item in player.current_room.items:
            print(
                f'There is a {Back.GREEN}{item.name}{Back.RESET} here. {item.description}')
    print('You can move in a direction (n/s/e/w), show (i)nventory, or (q)uit.')
    command: str = input(
        f'{Style.BRIGHT}|<>| What is your desire? |<>| ==>{Style.RESET_ALL}')
    command = command.lower().strip().split()
    if len(command) == 1:
        # Single word entered; only look at the first letter
        command = command[0][0]
        if command in ['n', 's', 'e', 'w']:
            # Go to the room, if possible
            player.go(command)
        elif command == 'i':
            # Look through the current inventory
            print(f'{Fore.YELLOW}|<>| Inventory |<>|')
            if len(player.items) > 0:
                for item in player.items:
                    print(
                        f'You have a {Back.GREEN}{item.name}{Back.RESET}. {item.description}')
            else:
                print('Your pockets are empty :(')
        elif command == 'q':
            # Leave this program
            print("Goodbye...")
            sys.exit()
        else:
            # Unused command
            print(f'{Fore.MAGENTA}|<>| Command misunderstood |<>|')
    else:
        # Multiple words entered; ideally in 'Verb Object' format
        commanded_object: str = command[1]
        if command[0] == 'get' or command[0] == 'take':
            # Pick up the item
            for it in player.current_room.items:
                if it.name == commanded_object:
                    it.on_get()
                    player.items.append(it)
                    player.current_room.items.remove(it)
                    break
            else:
                print(f'{Fore.CYAN}That item was not found.')
        elif command[0] == 'drop' or command[0] == 'lose':
            # Leave the item in the room
            for it in player.items:
                if it.name == commanded_object:
                    it.on_drop()
                    player.items.remove(it)
                    player.current_room.items.append(it)
                    break
            else:
                print(f'{Fore.CYAN}That item was not found.')
        else:
            # Unused command
            print(f'{Fore.MAGENTA}|<>| Command misunderstood |<>|')
