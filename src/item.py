

# Create a file called item.py and add an Item class in there.
# The item should have name and description attributes.
# Hint: the name should be one word for ease in parsing later.
# This will be the base class for specialized item types to be declared later.
class Item:
    '''This is the Item class'''

    def __init__(self, name, description):
        '''This is the default constructor'''
        self.name = name
        self.description = description

    def __str__(self):
        '''This is the overloaded String method'''
        return f'Name: {self.name}\nDescription: {self.description}'

    def on_get(self):
        '''This method runs when an item is picked up'''
        print(f'You have picked up a {self.name}.')

    def on_drop(self):
        '''This method runs when an item is dropped'''
        print(f'You have dropped the {self.name}.')
