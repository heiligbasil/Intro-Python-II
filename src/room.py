

# Implement a class to hold room information. This should have name and
# description attributes.
class Room:
    '''
    This is the Room class
    '''
    def __init__(self, name, description):
        '''
        This is the default constructor
        '''
        self.name = name
        self.description = description
        self.n_to: Room = None
        self.s_to: Room = None
        self.e_to: Room = None
        self.w_to: Room = None

    def __str__(self):
        '''
        This is the string method
        '''
        return f'Name: {self.name}\nDescription: {self.description}'
