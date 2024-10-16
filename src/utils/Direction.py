from enum import Enum

class Direction(Enum):
    INVALID = -1
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def is_valid(self):
        return self.name != 'INVALID'

    def inverse(self):
       if self.name == 'NORTH': return Direction.SOUTH
       if self.name == 'EAST': return Direction.WEST
       if self.name == 'SOUTH': return Direction.NORTH
       if self.name == 'WEST': return Direction.EAST

def convert_to_direction(other):
   dir = Direction.INVALID

   if   other in {Direction.NORTH, 0, 'n', 'north', 'NORTH'}: dir = Direction.NORTH
   elif other in {Direction.EAST, 1, 'e', 'east', 'EAST'}: dir = Direction.EAST
   elif other in {Direction.SOUTH, 2, 's', 'south', 'SOUTH'}: dir = Direction.SOUTH
   elif other in {Direction.WEST, 3, 'w', 'west', 'WEST'}: dir = Direction.WEST
   
   return dir