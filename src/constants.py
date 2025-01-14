from PIL import Image
from src.tiles.tile import Tile


ERROR_BACKGROUND_TILE: Tile = Tile(Image.new(mode='RGB', size=(40, 40), color='magenta'))