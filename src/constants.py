'''
constants used in other modules
'''
from PIL import Image
from src.direction import Direction
from src.tiles.tile import Tile

# if cell cannot collapse successfully, chose this image to display
ERROR_BACKGROUND_TILE: Tile = Tile(Image.new(mode='RGB', size=(40, 40), color='magenta'))

# on cell collapse, reduce possibilities in these neighboring cells
VALID_REDUCE_MOVES = [
        (-1,  0, Direction.SOUTH), # one cell to the NORTH of collapse
        ( 0,  1, Direction.WEST), # one cell to the EAST of collapse
        ( 1,  0, Direction.NORTH), # one cell to the SOUTH of collapse
        ( 0, -1, Direction.EAST) # one cell to the WEST of collapse
    ]
