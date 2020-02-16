import sys
import textwrap
from room import Room
from player import Player
from item import Item, LightSource
from colorama import Fore, Back, Style
import colorama


# Initialize the ANSI engine for Windows | https://github.com/tartley/colorama
colorama.init(autoreset=True)


# Declare all the rooms
room_list = {
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
room_list['outside'].n_to = room_list['foyer']
room_list['foyer'].s_to = room_list['outside']
room_list['foyer'].n_to = room_list['overlook']
room_list['foyer'].e_to = room_list['narrow']
room_list['overlook'].s_to = room_list['foyer']
room_list['narrow'].w_to = room_list['foyer']
room_list['narrow'].n_to = room_list['treasure']
room_list['treasure'].s_to = room_list['narrow']


# Declare all of the items
item_list = [Item('torch', 'A dry torch with only the top burnt.'),
             Item('matchbook', 'A full book of dry intact matches.'),
             Item('rope', 'A coiled sturdy-looking dry twisted rope of twine.'),
             Item('dagger', 'A rusting and blunt weapon in a sheath.'),
             LightSource("flamer", "A flaming torch provides orange flickering illumination.")]


# Link the items to the rooms
room_list['foyer'].items = [item_list[0]]
room_list['overlook'].items = [item_list[1]]
room_list['narrow'].items = [item_list[2]]
room_list['treasure'].items = [item_list[3]]


# Determine if there is enough light available to see
def enough_illumination():
    if player.current_room.is_illuminated:
        return True
    elif found_lightsource(player.current_room.items):
        return True
    elif found_lightsource(player.items):
        return True
    return False


# Search items for a LightSource
def found_lightsource(these_items: list):
    for each_item in these_items:
        if isinstance(each_item, LightSource):
            return True
    return False


# Determine if a string exists in a list of items and if so return the index
def item_index_in_list(this_list: list, text: str):
    index_of_item: int = None
    for item in this_list:
        if item.name == text:
            index_of_item = this_list.index(item)

    return index_of_item


#
# Main
#


# Make a new player object that is currently in the 'outside' room.
player: Player = Player(input("What's your name? ")
                        or 'Kowalksi', room_list['outside'])
print(f'{Back.WHITE}{Fore.BLACK}Welcome, {player.name} :)')


# REPL command loop - the game's engine
while True:
    print(f'{Fore.BLUE}|<>| Location |<>|')
    print(f"{player.name}'s current location is {Back.MAGENTA}{player.current_room.name}{Back.RESET}.")
    if (enough_illumination()):
        print(textwrap.TextWrapper(width=65).fill(
            player.current_room.description))
        if len(player.current_room.items) > 0:
            for item in player.current_room.items:
                print(
                    f'There is a {Back.GREEN}{item.name}{Back.RESET} here. {item.description}')
    else:
        print(f"{Back.BLACK}{Fore.WHITE}{Style.BRIGHT}It's pitch black!")
    print(
        f'You have {Fore.YELLOW}{player.xp}{Fore.RESET} XP and can move in a direction (n/s/e/w), get/drop/use items, show (i)nventory, or (q)uit.')
    command: str = input('|<>| What is your desire? |<>| ==> ')
    command = command.lower().strip().split()
    if len(command) == 1:
        # Single word entered; only look at the first letter
        command = command[0][0]
        if command in ['n', 's', 'e', 'w']:
            # Go to the room, if possible
            player.go(command, enough_illumination())
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
                    player.xp += 2
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
                    player.xp += 1
                    break
            else:
                print(f'{Fore.CYAN}That item was not found.')
        elif command[0] == 'use' or command[0] == 'activate':
            # Manipulate an effect using items in the inventory
            effected_object: str = command[-1]
            index_of_item_1 = item_index_in_list(
                player.items, commanded_object)
            index_of_item_2 = item_index_in_list(player.items, effected_object)
            if index_of_item_1 != None and index_of_item_2 != None:
                # Verified both items exist in the player's inventory
                if commanded_object == 'matchbook' and effected_object == 'torch':
                    # Light the torch on fire by combining two items to birth a new one
                    player.items.pop(index_of_item_1)
                    player.items.pop(index_of_item_2)
                    player.items.append(item_list[4])
                    player.xp += 5
                    print(
                        f'{Fore.GREEN}Your ingenuity has produced a {Fore.YELLOW}{item_list[4].name}{Fore.RESET}.')
                else:
                    print(
                        f"{Fore.MAGENTA}I don't understand how a {commanded_object} can activate a {effected_object}.")
            else:
                # Items specified are not in the player's inventory
                if index_of_item_1 == None:
                    print(
                        f"{Fore.MAGENTA}You aren't carrying a {commanded_object}.")
                if index_of_item_2 == None:
                    print(f"{Fore.MAGENTA}You aren't carrying a {effected_object}.")
        else:
            # Unused command
            print(f'{Fore.MAGENTA}|<>| Command misunderstood |<>|')
