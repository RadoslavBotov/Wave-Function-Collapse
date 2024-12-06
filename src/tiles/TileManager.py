import os
from tiles.Tile import Tile

from loaders.ConfigParser import ConfigParser
from loaders.ImageLoader import ImageLoader

class TileManager:
    def __init__(self, image_size, tile_path, tile_descriptor):
        self.image_size = image_size
        self.tile_path = tile_path
        self.tile_descriptor = tile_descriptor
        self.tiles = []

    def create_tiles(self, tile_set):
        configs = self.__load_tile_configs(tile_set)
        images = self.__load_images(tile_set)
        
        for name in configs:
            permissions = configs.get(name)
            valid_perms = self.__init_perms(permissions)

            for i in range(permissions.get('rotations')):
                tile = Tile(images[name], valid_perms)
                tile.rotate_tile(i)
                self.tiles.append(tile)

    def __load_tile_configs(self, tile_set):
        parser = ConfigParser(os.path.join(self.tile_path, tile_set, self.tile_descriptor))
        parser.parse()
        return parser.config

    def __load_images(self, tile_set):
        loader = ImageLoader(os.path.join(self.tile_path, tile_set))
        loader.load()
        return loader.images

    def __init_perms(self, perms):
        return [perms.get('north'), perms.get('east'), perms.get('south'), perms.get('west')]