from enum import Enum
from room import Room


# Associate each direction with its cardinal identifier
class Cardinal(Enum):
    North = 'n'
    South = 's'
    East = 'e'
    West = 'w'


# Write a class to hold player information, e.g. what room they are in
# currently.
class Player:
    '''This is the Player class'''
    def __init__(self, name, starting_room):
        '''This is the default constructor'''
        self.name = name
        self.current_room = starting_room

    def go(self, direction):
        '''This defines Player movement'''
        go_to_room: Room = getattr(self.current_room, f'{direction}_to')
        cardinal: Cardinal = Cardinal(direction).name
        if go_to_room:
            self.current_room = go_to_room
            message = f'{self.name} has moved {cardinal}.'
        else:
            message = f'{self.name} cannot move {cardinal}.'
        print(message)
