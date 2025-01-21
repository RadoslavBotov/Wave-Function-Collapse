from PIL import Image
from src.direction import Direction
from src.tiles.tile_set import TileSet
from src.tiles.tile import Tile

# ==========================================================================
# we can think of t1 as the original tile, and t2-t4, as its three rotations
# t1 = Tile(sides_code='111000000000')
# t2 = Tile(sides_code='000000000111')
# t3 = Tile(sides_code='000000111000')
# t4 = Tile(sides_code='000111000000')

# ==========================================================================

def test_get_tile_image_size_empty():
    # Arange
    tile_set = TileSet()
    
    # Act
    size = tile_set.get_tile_image_size()
    
    # Assert
    assert size is None


def test_get_tile_image_size_no_images():
    # Arange
    t1 = Tile(sides_code='111000000000')
    t2 = Tile(sides_code='000000000111')
    t3 = Tile(sides_code='000000111000')
    t4 = Tile(sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    
    # Act
    size = tile_set.get_tile_image_size()
    
    # Assert
    assert size is None


def test_get_tile_image_size_with_images_1():
    # Arange
    image = Image.new('RGB', (40, 40))
    tile = Tile(image)
    tile_set = TileSet([tile])
    
    # Act
    size = tile_set.get_tile_image_size()
    
    # Assert
    assert size == (40, 40)


def test_get_tile_image_size_with_images_2():
    # Arange
    image1 = Image.new('RGB', (40, 90))
    image2 = Image.new('RGB', (40, 90))
    t1 = Tile(image1)
    t2 = Tile(image2)
    tile_set = TileSet([t1, t2])
    
    # Act
    size = tile_set.get_tile_image_size()
    
    # Assert
    assert size == (40, 90)

# ==========================================================================

def test_resize_tiles_no_tiles():
    # Arange
    tile_set = TileSet()
    
    # Act
    result = tile_set.resize_tiles((40, 40))
    
    # Assert
    assert result is False


def test_resize_tiles_with_tiles():
    # Arange
    image1 = Image.new('RGB', (40, 40))
    image2 = Image.new('RGB', (40, 40))
    t1 = Tile(image1)
    t2 = Tile(image2)
    tile_set = TileSet([t1, t2])
    
    # Act
    result = tile_set.resize_tiles((80, 80))
    size = tile_set.get_tile_image_size()
    
    # Assert
    assert result is True
    assert size == (80, 80)

# ==========================================================================
'''
Explainging following tests:
- each test compares a side of t1 to the rest of tiles in tile_set
- each test has a description, showing the code of t1 corresponding to given direction
  and a list of codes, corresponding to given direction, for each tile in tile_set in the order t1, t2, t3, t4

'''

def test_get_reduced_tile_set_north_south():
    '''
    NORTH t1: 111
    SOUTH tile_set: aaa aaa 111 aaa
    => only 1 match
    '''
    # Arange
    other_direction = Direction.NORTH
    tile_set_direction = Direction.SOUTH
    t1 = Tile(sides_code='111aaaaaaaaa')
    t2 = Tile(sides_code='aaaaaaaaa111')
    t3 = Tile(sides_code='aaaaaa111aaa')
    t4 = Tile(sides_code='aaa111aaaaaa')
    tile_set = TileSet([t1, t2, t3, t4])
    
    # Act
    reduced_tile_set = tile_set.get_reduced_tile_set(t1, tile_set_direction, other_direction)
    
    # Assert
    assert str(reduced_tile_set) == '[<sides_code=aaaaaa111aaa, image=None>]'


def test_get_reduced_tile_set_south_north():
    '''
    SOUTH t1: aaa
    NORTH tile_set: 111 aaa aaa aaa
    => 3 matches
    '''
    # Arange
    other_direction = Direction.SOUTH
    tile_set_direction = Direction.NORTH
    t1 = Tile(sides_code='111aaaaaaaaa')
    t2 = Tile(sides_code='aaaaaaaaa111')
    t3 = Tile(sides_code='aaaaaa111aaa')
    t4 = Tile(sides_code='aaa111aaaaaa')
    tile_set = TileSet([t1, t2, t3, t4])
    
    # Act
    reduced_tile_set = tile_set.get_reduced_tile_set(t1, tile_set_direction, other_direction)
    
    # Assert
    assert str(reduced_tile_set) == '[<sides_code=aaaaaaaaa111, image=None>, <sides_code=aaaaaa111aaa, image=None>, <sides_code=aaa111aaaaaa, image=None>]'


def test_get_reduced_tile_set_east_west():
    '''
    EAST t1: aaa
    WEST tile_set: aaa 111 aaa aaa
    => 3 matches
    '''
    # Arange
    other_direction = Direction.EAST
    tile_set_direction = Direction.WEST
    t1 = Tile(sides_code='111aaaaaaaaa')
    t2 = Tile(sides_code='aaaaaaaaa111')
    t3 = Tile(sides_code='aaaaaa111aaa')
    t4 = Tile(sides_code='aaa111aaaaaa')
    tile_set = TileSet([t1, t2, t3, t4])
    
    # Act
    reduced_tile_set = tile_set.get_reduced_tile_set(t1, tile_set_direction, other_direction)
    
    # Assert
    assert str(reduced_tile_set) == '[<sides_code=111aaaaaaaaa, image=None>, <sides_code=aaaaaa111aaa, image=None>, <sides_code=aaa111aaaaaa, image=None>]'


def test_get_reduced_tile_set_west_east():
    '''
    WEST t1: aaa
    EAST tile_set: aaa aaa aaa 111
    => 3 matches
    '''
    # Arange
    other_direction = Direction.WEST
    tile_set_direction = Direction.EAST
    t1 = Tile(sides_code='111aaaaaaaaa')
    t2 = Tile(sides_code='aaaaaaaaa111')
    t3 = Tile(sides_code='aaaaaa111aaa')
    t4 = Tile(sides_code='aaa111aaaaaa')
    tile_set = TileSet([t1, t2, t3, t4])
    
    # Act
    reduced_tile_set = tile_set.get_reduced_tile_set(t1, tile_set_direction, other_direction)
    
    # Assert
    assert str(reduced_tile_set) == '[<sides_code=111aaaaaaaaa, image=None>, <sides_code=aaaaaaaaa111, image=None>, <sides_code=aaaaaa111aaa, image=None>]'
