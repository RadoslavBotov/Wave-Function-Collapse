'''
TileSetManager dict implementation
'''
from src.tiles.tile_set import TileSet


class TileSetManager(dict[str, TileSet]):
    '''
    qwe
    '''
    def __init__(self, *args, **kwargs):
        '''
        A dict of TileSets.
        Format should be {'tile_set_name': TileSet}.
        '''
        super(TileSetManager, self).__init__(*args, **kwargs)


    def get_tile_set_image_size(self, tile_set_name: str) -> tuple[int, int]|None:
        '''
        Returns the size of a Tile in a TileSet.
        
        If TileSetManager is empty, returns None.
        If TileSetManager doesn't contain tile_set_name, returns None.
        Otherwise, returns image size (width, height).

        - tile_set_name - name of TileSet, whose image size to be returned
        '''
        if len(self) == 0 or tile_set_name not in self:
            return None

        return self[tile_set_name].get_tile_image_size()


    def resize_tile_set(self, tile_set_name: str, new_size: tuple[int, int]) -> bool|None:
        '''
        Resizes all images in given TileSet.
        
        If TileSetManager is empty, returns None.
        If TileSetManager doesn't contain tile_set_name, returns None.
        If all tiles have an image and resize succeeds, returns True.
        Otherwise, returns False.

        - tile_set_name - name of TileSet, whose image size to be returned
        - new_size - new size of tiles' images
        '''
        if len(self) == 0 or tile_set_name not in self:
            return None

        return self[tile_set_name].resize_tiles(new_size)
