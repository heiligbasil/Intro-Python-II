

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
