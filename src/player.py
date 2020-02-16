from enum import Enum
from room import Room
from item import Item, LightSource


# Associate each direction with its cardinal identifier
class Cardinal(Enum):
    North = 'n'
    South = 's'
    East = 'e'
    West = 'w'


# Write a class to hold player information,
# e.g. what room they are in currently.
class Player:
    '''This is the Player class'''

    def __init__(self, name, starting_room, xp=0):
        '''This is the default constructor'''
        self.name: str = name
        self.current_room: Room = starting_room
        self.xp: int = xp
        self.items: list = []

    def go(self, direction, illumination):
        '''This defines Player movement'''
        go_to_room: Room = getattr(self.current_room, f'{direction}_to')
        cardinal: str = Cardinal(direction).name
        message: str = f'{self.name} cannot move {cardinal}.'
        if go_to_room:
            # First validate that a real path was chosen
            room_lightsource: bool = go_to_room.is_illuminated
            item_lightsource: bool = False
            for item in go_to_room.items:
                if isinstance(item, LightSource):
                    # Try to see if any of the items in the next room are a LightSource
                    item_lightsource = True
            if not illumination and not room_lightsource and not item_lightsource:
                # Bar movement only if the current room is dark and there is no
                # source of light in the direction that the player is moving in.
                message = 'The way is pitch black!'
            else:
                self.current_room = go_to_room
                message = f'{self.name} has moved {cardinal}.'
                self.xp += 1
        print(message)
