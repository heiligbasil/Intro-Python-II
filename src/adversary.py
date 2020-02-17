

# Base class for natural hazards and monsters affecting the player
class Adversary:
    '''This is the parent class'''
    name: str
    description: str
    harm_amount: int
    harm_message: str
    injured_message: str
    health: int


class Hazard(Adversary):
    '''This child class inherits from the parent class'''

    def __init__(self, name: str, description: str, harm_amount: int, harm_message: str, injured_message: str):
        '''The default constructor for the hazard class'''
        self.name = name
        self.description = description
        self.harm_amount = harm_amount
        self.harm_message = harm_message
        self.injured_message = injured_message
        self.health = None


class Monster(Adversary):
    '''This child class inherits from the parent class'''

    def __init__(self, name: str, description: str, harm_amount: int, harm_message: str, injured_message: str, health: int):
        '''The default constructor for the monster class'''
        self.name = name
        self.description = description
        self.harm_amount = harm_amount
        self.harm_message = harm_message
        self.injured_message = injured_message
        self.health = health

    def decrease_health(self, injury_amount: int):
        '''This harms the Monster and sees if it is dead'''
        self.health -= injury_amount
        if self.health < 1:
            # Monster died
            return True
        return False
