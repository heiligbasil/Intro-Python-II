import sys
import textwrap
from room import Room
from player import Player


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


#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player: Player = Player("Kowalksi", room['outside'])


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
    print()
    print(f"{player.name}'s current location is {player.current_room.name}.")
    print(textwrap.TextWrapper(width=50).fill(player.current_room.description))
    command: chr = input("== Where do you want to move? == (n/s/e/w) > ")
    command = command.upper()
    if command == 'N':
        if player.current_room.n_to is None:
            print(f'{player.name} cannot move North.')
        else:
            print(f'{player.name} has moved North.')
            player.current_room = player.current_room.n_to
    elif command == 'S':
        if player.current_room.s_to is None:
            print(f'{player.name} cannot move South.')
        else:
            print(f'{player.name} has moved South.')
            player.current_room = player.current_room.s_to
    elif command == 'E':
        if player.current_room.e_to is None:
            print(f'{player.name} cannot move East.')
        else:
            print(f'{player.name} has moved East.')
            player.current_room = player.current_room.e_to
    elif command == 'W':
        if player.current_room.w_to is None:
            print(f'{player.name} cannot move West.')
        else:
            print(f'{player.name} has moved West.')
            player.current_room = player.current_room.w_to
    elif command == 'Q':
        print("Goodbye...")
        sys.exit()
    else:
        print("|<>|Command misunderstood|<>|")
