from enum import IntEnum


class Direction(IntEnum):
    INVALID = -1
    
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


    def is_valid(self) -> bool:
        return self is not Direction.INVALID


    def get_opposite(self) -> 'Direction':
        match self:
           case Direction.NORTH: return Direction.SOUTH
           case Direction.EAST : return Direction.WEST
           case Direction.SOUTH: return Direction.NORTH
           case Direction.WEST : return Direction.EAST
        
        return Direction.INVALID