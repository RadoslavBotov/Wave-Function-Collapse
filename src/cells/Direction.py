from enum import IntEnum


class Direction(IntEnum):
    INVALID = -1
    
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


    def is_valid(self) -> bool:
        return self.value != -1


    def inverse(self) -> 'Direction':
        match self:
           case Direction.NORTH: return Direction(2)
           case Direction.EAST : return Direction(3)
           case Direction.SOUTH: return Direction(0)
           case Direction.WEST : return Direction(1)
        
        return Direction.INVALID