import sys
import textwrap
from room import Room
from player import Player
from item import Item, LightSource
from adversary import Adversary, Hazard, Monster
from colorama import Fore, Back, Style
import colorama


# Initialize the ANSI engine for Windows | https://github.com/tartley/colorama
colorama.init(autoreset=True)


# Declare all the rooms
room_list = {
    'outside':  Room("Outside Cave Entrance", "North of you, the cave mount beckons."),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you,
falling into the darkness. Ahead to the north, a light flickers in the distance,
but there is no way across the chasm. Brambles to the west."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),

    'bramble': Room('Brambly Outcropping', """A perilous ledge strewn with rocks leading
downwards to the west which is overgrown with brambles and thorns. It looks dangerous."""),

    'holly': Room('Holly Outcropping', """The narrow ledge continues westward with overgrown
holly bushes and thorns. Coninuing west will not be pleasant."""),

    'nettles': Room('Nettles Outcropping', """Stinging nettles, poison oak, and
poison ivy cover the path forward. Brushing against the plants is unavoidable. The path seems
to curve north and incline east."""),

    'junction': Room('Cliff Base Junction', """The base of the towering cliff.
Rocks, femurs, and various artifacts are embedded in the ground. To the west is 
a forest, to the north is a path leading into darkness, to the east follows a 
path along the cliffside, to the south is the painful path back up to the top.""")
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
room_list['overlook'].w_to = room_list['bramble']
room_list['bramble'].w_to = room_list['holly']
room_list['bramble'].e_to = room_list['overlook']
room_list['holly'].w_to = room_list['nettles']
room_list['holly'].e_to = room_list['bramble']
room_list['nettles'].n_to = room_list['junction']
room_list['nettles'].e_to = room_list['holly']
room_list['junction'].s_to = room_list['nettles']


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


# Declare all of the adversaries
adversary_list: dict = {
    'bramble': Hazard('Bramble', 'Brambles and thorny bushes stick and scratch!', 1,
                      'The brambles and thorny bushes are sticking and scratching you!',
                      'Your attempts at harming these brambles result in further sticking and scratching!'),

    'holly': Hazard('Holly', 'Holly leaves prick and poke!', 1,
                    'The holly leaves are pricking and poking you!',
                    'Your attempts at harming these holly bushes result in further pricking and poking!'),

    'nettle': Hazard('Nettle', 'Stinging nettles and poison plants are nocuous and noxious!', 1,
                     'The stinging nettles are poisoning you!',
                     'Your attempts at harming these stinging nettles and poisonous plants results in further poisoning!'),

    'bat': Monster('Bat', 'Bats bite and spread plagues!', 2,
                   'The bat is biting and scratching you!',
                   'You attack the crazy bat!', 1),

    'mouse': Monster('Mouse', 'Mice gnaw and carry disease!', 2,
                     'The mouse is gnawing and scratching you!',
                     'You attack the poor mouse!', 1)
}


# Link the adversaries to the rooms
room_list['bramble'].adversaries.append(adversary_list['bramble'])
room_list['holly'].adversaries.append(adversary_list['holly'])
room_list['nettles'].adversaries.append(adversary_list['nettle'])
room_list['junction'].adversaries.append(adversary_list['bat'])
room_list['junction'].adversaries.append(adversary_list['mouse'])

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


# Check for existing adversaries
def threat_of_adversaries(this_list: list):
    if (len(this_list) > 0):
        return True


# Deal harm to player for each adversary
def deal_harm_from_adversaries(this_list: list):
    for adversary in this_list:
        print(adversary.harm_message, end=' ')
        print(f'{Back.RED}{adversary.name}{Back.RESET} does {Fore.RED}{adversary.harm_amount}{Fore.RESET} HP harm to you!')
        if player.decrease_hp(adversary.harm_amount):
            return True
    return False


#
# Main
#


# Make a new player object that is currently in the 'outside' room.
player: Player = Player(input("What's your name? ")
                        or 'Kowalksi', room_list['outside'])
print(f'{Back.WHITE}{Fore.BLACK}Welcome, {player.name} :)')


# REPL command loop - the game's engine
while True:
    print(f'{Fore.BLUE}|<>| Setting |<>|')
    print(f"{player.name}'s current location is {Back.MAGENTA}{player.current_room.name}{Back.RESET}.")
    if (enough_illumination()):
        print(textwrap.TextWrapper(width=65).fill(
            player.current_room.description))
        if len(player.current_room.adversaries) > 0:
            for adversary in player.current_room.adversaries:
                print(
                    f'There is a {Back.RED}{adversary.name}{Back.RESET} here. {adversary.description}')
        if len(player.current_room.items) > 0:
            for item in player.current_room.items:
                print(
                    f'There is a {Back.GREEN}{item.name}{Back.RESET} here. {item.description}')
    else:
        print(f"{Back.BLACK}{Fore.WHITE}{Style.BRIGHT}It's pitch black!")
    if threat_of_adversaries(player.current_room.adversaries):
        if deal_harm_from_adversaries(player.current_room.adversaries):
            print(f'{Fore.RED}You have died...{Fore.RESET}')
            sys.exit()
    print(f"""You have {Fore.YELLOW}{player.xp}{Fore.RESET} XP, \
{Fore.YELLOW}{player.current_hp}{Fore.RESET} HP, \
and can move in a direction (n/s/e/w), get/drop/use items, (a)ttack, (i)nventory, or (q)uit.""")
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
        elif command == 'a':
            print(
                f'{Fore.CYAN}Attack what?{Fore.RESET} (Specify the name of your fury.)')
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
                    player.increase_xp(2)
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
                    player.increase_xp(1)
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
                    player.increase_xp(5)
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
        elif command[0] == 'attack' or command[0] == 'a':
            # Attack the specified adversary
            if player.attack_adversary(commanded_object):
                # Either the monster died or the player died
                adversary: Adversary = None
                for this_adversary in player.current_room.adversaries:
                    if this_adversary.name.lower() == commanded_object:
                        # Grab the adversary
                        adversary = this_adversary
                if adversary.health < 1:
                    print(f'{Fore.GREEN}You have vanquished a {adversary.name}!')
                    player.current_room.adversaries.remove(adversary)
                if player.current_hp < 1:
                    print(
                        f'A {adversary.name} was your downfall. {Fore.RED}You have died...{Fore.RESET}')
                    sys.exit()
        else:
            # Unused command
            print(f'{Fore.MAGENTA}|<>| Command misunderstood |<>|')
