

# Base class for natural hazards and monsters affecting the player
class Adversary:
    '''This is the parent class'''
    name: str
    description: str
    harm: int
    health: int


class Hazard(Adversary):
    '''This child class inherits from the parent class'''

    def __init__(self, name: str, description: str, harm: int):
        '''The default constructor for the hazard class'''
        self.name = name
        self.description = description
        self.harm = harm
        self.health = None


class Monster(Adversary):
    '''This child class inherits from the parent class'''

    def __init__(self, name: str, description: str, harm: int, health: int):
        '''The default constructor for the monster class'''
        self.name = name
        self.description = description
        self.harm = harm
        self.health = health
