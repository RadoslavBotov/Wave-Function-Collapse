from PIL import Image
from src.tiles.tile import Tile


class TileSet(list['Tile']):
    '''
    A collection of tiles with the same theme.
    '''
    def __init__(self, *args, **kwargs) -> None:
        super(TileSet, self).__init__(*args, **kwargs)


    def get_tile_image_size(self) -> None|int:
        '''
        As all images have same size, returns first tile image size.
        If @tile.image is None, returns None.
        Otherwise returns size of image.
        '''
        if len(self) == 0:
            return None
        
        return self[0].get_image_size()


    def resize_tiles(self, new_size: int) -> None:
        for tile in self:
            tile.resize_image(new_size)


    @classmethod
    def create_tile_set(cls, configs: dict, images: dict[str, Image.Image]) -> 'TileSet':
        '''
        Factory method for creating a TileSet.

        - name - tile set name
        - configs - 
        - images - 
        '''
        tiles = []

        for image_name in configs:
            image_configs = configs[image_name]
            side_codes = image_configs['directions']

            original_tile = Tile(images[image_name], side_codes)
            tiles.append(original_tile)

            for rotations_amount, rotation_direction in image_configs['rotations']:
                rotated_tile = Tile(images[image_name], side_codes)
                rotated_tile.rotate_tile(rotations_amount, rotation_direction)
                tiles.append(rotated_tile)

        return TileSet(tiles)
