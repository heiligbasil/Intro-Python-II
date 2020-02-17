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
    xp: int = 0
    current_hp: int = 10
    max_hp: int = current_hp

    def __init__(self, name, starting_room):
        '''This is the default constructor'''
        self.name: str = name
        self.current_room: Room = starting_room
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
                self.increase_xp(1)
        print(message)

    def increase_xp(self, amount: int):
        '''This increments the player's XP by the specified amount'''
        self.xp += amount

    def decrease_hp(self, amount: int):
        '''This decreases the player's HP by the specified amount'''
        self.current_hp -= amount
        if self.current_hp < 1:
            # Player died
            return True
        return False

    def increase_hp(self, amount: int):
        '''This increases the player's HP by the specified amount'''
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            # Don't allow HP to go over the max
            self.current_hp = self.max_hp
