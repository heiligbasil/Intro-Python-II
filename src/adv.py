import sys
import textwrap
from room import Room
from player import Player
from item import Item

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
player: Player = Player(input("What's your name? ") or "Kowalksi",
                        room['outside'])
print(f"Welcome, {player.name} :)")

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.


while True:
    print('|<>| Location |<>|')
    print(f"{player.name}'s current location is {player.current_room.name}.")
    print(textwrap.TextWrapper(width=50).fill(player.current_room.description))
    if len(player.current_room.items) > 0:
        for item in player.current_room.items:
            print(f'There is a {item.name} here. {item.description}')
    print('You can move in a direction (n/s/e/w), show (i)nventory, or (q)uit.')
    command: str = input('|<>| What is your desire? |<>| ==> ')
    command = command.lower().strip()[0]
    if command in ['n', 's', 'e', 'w']:
        # Go to the room, if possible
        player.go(command)
    elif command == 'i':
        # Look through the current inventory
        if len(player.items) > 0:
            print('|<>| Inventory |<>|')
            for item in player.items:
                print(f'You have a {item.name}. {item.description}')
        else:
            print('Your pockets are empty :(')
    elif command == 'q':
        # Leave this program
        print("Goodbye...")
        sys.exit()
    else:
        # Unused command
        print("|<>| Command misunderstood |<>|")
