from tiles.Tile import Tile

from utils.ConfigParser import ConfigParser
from utils.ImageLoader import ImageLoader

class TileManager:
    def __init__(self, image_size = 40, tile_path = 'src/resources/basic_tiles', tile_descriptions = 'tile_descriptions.yaml'):
        self.image_size = image_size
        self.tile_path = tile_path
        self.tile_descriptions = tile_descriptions
        self.tiles = []

    def create_tiles(self):
        configs = self.__load_tile_configs()
        images = self.__load_images()
        
        for name in configs:
            permissions = configs.get(name)
            valid_perms = self.__init_perms(permissions)

            for i in range(permissions.get('rotations')):
                rotatedImage = images[name].rotate(90 * i)
                tile = Tile(rotatedImage, valid_perms)
                tile.rotate_permissions(i)
                self.tiles.append(tile)

    def __load_tile_configs(self):
        parser = ConfigParser(f'{self.tile_path}/{self.tile_descriptions}')
        parser.parse()
        return parser.config

    def __load_images(self):
        loader = ImageLoader(self.tile_path)
        loader.load()
        return loader.images

    def __init_perms(self, perms):
        return [perms.get('north'), perms.get('east'), perms.get('south'), perms.get('west')]

"""
# Load tiles and rotations
for f in os.listdir(tiles_path): 
    if f.endswith('.png'):
        image = Image.open(tiles_path + '/' + f).resize((M,M))
        *permissions, rotations = loaded.get(f[:-4]).values()
        for i in range(rotations):
            rotatedImage = image.rotate(90 * i)
            tiles.append(Tile(ImageTk.PhotoImage(rotatedImage), permissions, rotate=i))
"""
