from enum import IntEnum

class Direction(IntEnum):
    invalid = -1
    
    north = 0
    n = 0

    east = 1
    e = 1

    south = 2
    s = 2

    west = 3
    w = 3

    def is_valid(self):
        return self.value != -1

    def inverse(self):
       match self.name:
           case 'north': return Direction.south
           case 'east' : return Direction.west
           case 'south': return Direction.north
           case 'west' : return Direction.east