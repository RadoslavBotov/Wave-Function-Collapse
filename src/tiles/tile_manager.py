from src.tiles.tile import Tile

NORTH = 'north'

class TileManager:
    def __init__(self, image_size):
        self.image_size = image_size
        self.tiles = []


    def create_tiles(self, configs, images):
        for name in configs:
            permissions = configs.get(name)
            valid_perms = self.__init_perms(permissions)

            for i in range(permissions.get('rotations')):
                tile = Tile(images[name], valid_perms)
                tile.rotate_tile(i)
                self.tiles.append(tile)


    def __init_perms(self, perms):
        return [perms.get(NORTH), perms.get('east'), perms.get('south'), perms.get('west')]