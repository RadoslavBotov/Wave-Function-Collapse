'''
TileSet list implementation
'''
from src.direction import Direction
from src.tiles.tile import Tile


class TileSet(list[Tile]):
    '''
    A list of tiles with the same theme.
    '''
    def get_tile_image_size(self) -> tuple[int, int]|None:
        '''
        All images in TileSet should have the same size.
        Returns the first tile's image size.
        If TileSet is empty, returns None.
        '''
        if len(self) == 0:
            return None

        return self[0].get_image_size()


    def resize_tiles(self, new_size: tuple[int, int]) -> bool:
        '''
        Resizes image of each Tile in TileSet.
        
        If all tiles have an image and resize succeeds, returns True.
        Otherwise, returns False.

        - new_size - new size of tiles' images
        '''
        if len(self) == 0:
            return False

        return all(tile.resize_image(new_size) for tile in self)


    def get_reduced_tile_set(self,
                             other_tile: Tile,
                             tile_set_direction: Direction,
                             other_direction: Direction) -> 'TileSet':
        '''
        Removes Tile's from TileSet, whose sides_code do not match
        the sides_code of @other_tile on the given directions.

        - other_tile - tile whose sides_code are matched to TileSet
        - tile_set_direction - Direction of side for TileSet Tiles'
        - other_direction - Direction of side for other_tile
        '''
        return TileSet(
            tile
            for tile
            in self
            if tile.match_sides_code(other_tile, tile_set_direction, other_direction) is True
        )
