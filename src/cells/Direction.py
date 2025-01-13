from enum import IntEnum


class Direction(IntEnum):
    INVALID = -1

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


    def is_invalid(self) -> bool:
        '''
        Checks if instance is INVALID
        '''
        return self is Direction.INVALID


    def get_opposite(self) -> 'Direction':
        '''
        Returns the opposite cardinal direction.
        '''
        match self:
           case Direction.NORTH: return Direction.SOUTH
           case Direction.EAST : return Direction.WEST
           case Direction.SOUTH: return Direction.NORTH
           case Direction.WEST : return Direction.EAST

        return Direction.INVALID

    def get_slice(self, reverse: bool = False) -> slice:
        '''
        Gets a slice object corresponding to the index range of a Direction.
        
        - reverse - indicates if slice should be reversed
        
        - NORTH - index range of [0:2], first set of 3 character is sides_code
        - EAST - index range of [3:5], second set of 3 character is sides_code
        - SOUTH - index range of [6:8], third set of 3 character is sides_code
        - WEST - index range of [9:11], forth set of 3 character is sides_code
        '''
        start = 3 * self.value
        end = 3 * self.value + 3

        if reverse is False:
            return slice(start, end, 1)
        else:
            end -= 1
            start = start - 1 if start - 1 > 0 else None

            return slice(end, start, -1)
