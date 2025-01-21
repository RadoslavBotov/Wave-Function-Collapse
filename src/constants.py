from PIL import Image
from src.direction import Direction
from src.tiles.tile import Tile


ERROR_BACKGROUND_TILE: Tile = Tile(Image.new(mode='RGB', size=(40, 40), color='magenta'))

VALID_REDUCE_MOVES = [ 
        (-1,  0, Direction.SOUTH),
        ( 0,  1, Direction.WEST),
        ( 1,  0, Direction.NORTH),
        ( 0, -1, Direction.EAST)
    ]