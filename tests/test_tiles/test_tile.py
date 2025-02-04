from PIL import Image
import pytest
from src.direction import Direction
from src.tiles.tile import Tile

# ==========================================================================

def test_default_tile():
    # Arange
    tile = Tile()
    
    # Assert
    assert tile.image is None, 'image should be None'
    assert tile.sides_code == '!!!!!!!!!!!!', 'sides_code shoud be \'!!!!!!!!!!!!\''

# ==========================================================================

def test_get_rotated_image_none_image():
    # Arange
    tile = Tile(image=None)
    
    # Act
    rotated_image = tile._get_rotated_image() 
    
    # Assert
    assert rotated_image is None


def test_get_rotated_image_once_left():
    # Arange
    image = Image.new('RGB', (40, 80), 'green')
    tile = Tile(image=image)
    
    # Act
    rotated_image = tile._get_rotated_image(1) 
    
    # Assert
    assert rotated_image.size == (80, 40)


def test_get_rotated_image_once_right():
    # Arange
    image = Image.new('RGB', (40, 80), 'green')
    tile = Tile(image=image)
    
    # Act
    rotated_image = tile._get_rotated_image(1, 'right') 
    
    # Assert
    assert rotated_image.size == (80, 40)

# ==========================================================================

def test_get_shifted_sides_code_default():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code() 
    
    # Assert
    assert shifted_code == sides_code


def test_get_shifted_sides_code_3_left():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(3) 
    
    # Assert
    assert shifted_code == 'abc456def123'


def test_get_shifted_sides_code_6_left():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(6) 
    
    # Assert
    assert shifted_code == '456def123abc'


def test_get_shifted_sides_code_9_left():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(9) 
    
    # Assert
    assert shifted_code == 'def123abc456'


def test_get_shifted_sides_code_12_left():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(12) 
    
    # Assert
    assert shifted_code == '123abc456def'


def test_get_shifted_sides_code_3_right():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(3, 'right') 
    
    # Assert
    assert shifted_code == 'def123abc456'


def test_get_shifted_sides_code_6_right():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(6, 'right') 
    
    # Assert
    assert shifted_code == '456def123abc'


def test_get_shifted_sides_code_9_right():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(9, 'right') 
    
    # Assert
    assert shifted_code == 'abc456def123'


def test_get_shifted_sides_code_12_right():
    # Arange
    sides_code = '123abc456def'
    tile = Tile(None, sides_code)
    
    # Act
    shifted_code = tile._get_shifted_sides_code(12, 'right') 
    
    # Assert
    assert shifted_code == '123abc456def'
    
# ==========================================================================

def test_rotate_tile_invalid_direction():
    # Arange
    tile = Tile()
    
    # Act
    with pytest.raises(ValueError) as e:
        tile.rotate_tile(0, 'invalid_direction')
    
    # Assert
    assert str(e.value) == 'Invalid rotate_direction: invalid_direction'


def test_rotate_tile_no_rotation():
    # Arange
    image = Image.new('RGB', (40, 80))
    sides_code = '111+++111+++'
    tile = Tile(image, sides_code)
    
    # Act
    tile.rotate_tile(0, 'left')
    
    # Assert
    assert tile.image.size == (40, 80)
    assert tile.sides_code == '111+++111+++'


def test_rotate_tile_one_rotation():
    # Arange
    image = Image.new('RGB', (40, 80))
    sides_code = '111+++111+++'
    tile = Tile(image, sides_code)
    
    # Act
    tile.rotate_tile(1, 'left')
    
    # Assert
    assert tile.image.size == (80, 40)
    assert tile.sides_code == '+++111+++111'

# ==========================================================================

def test_get_image_size_no_image():
    # Arange
    tile = Tile(image=None)
    
    # Act
    image_size = tile.get_image_size()
    
    # Assert
    assert image_size is None


def test_get_image_size_square():
    # Arange
    image = Image.new('RGB', (40, 40))
    tile = Tile(image=image)
    
    # Act
    image_size = tile.get_image_size()
    
    # Assert
    assert image_size == (40, 40)


def test_get_image_size_rect():
    # Arange
    image = Image.new('RGB', (40, 80))
    tile = Tile(image=image)
    
    # Act
    image_size = tile.get_image_size()
    
    # Assert
    assert image_size == (40, 80)
    
# ==========================================================================

def test_resize_image_none_image():
    # Arange
    tile = Tile(image=None)
    
    # Act
    result = tile.resize_image((40, 40))
    
    # Assert
    assert result is False


def test_resize_image_smaller():
    # Arange
    image = Image.new('RGB', (40, 40))
    tile = Tile(image=image)
    
    # Act
    result = tile.resize_image((20, 20))
    
    # Assert
    assert result is True
    assert tile.image is not None
    assert tile.image.size == (20, 20)


def test_resize_image_bigger():
    # Arange
    image = Image.new('RGB', (40, 40))
    tile = Tile(image=image)
    
    # Act
    result = tile.resize_image((80, 80))
    
    # Assert
    assert result is True
    assert tile.image is not None
    assert tile.image.size == (80, 80)

# ==========================================================================

def test_get_code_group_north():
    # Arange
    sides_code = '123abc456def'
    direction = Direction.NORTH
    tile = Tile(sides_code=sides_code)
    
    # Act
    code_group = tile.get_code_group(direction)
    
    # Assert
    assert code_group == '123'


def test_get_code_group_east():
    # Arange
    sides_code = '123abc456def'
    direction = Direction.EAST
    tile = Tile(sides_code=sides_code)
    
    # Act
    code_group = tile.get_code_group(direction)
    
    # Assert
    assert code_group == 'abc'
    
    
def test_get_code_group_south():
    # Arange
    sides_code = '123abc456def'
    direction = Direction.SOUTH
    tile = Tile(sides_code=sides_code)
    
    # Act
    code_group = tile.get_code_group(direction)
    
    # Assert
    assert code_group == '456'
    
    
def test_get_code_group_west():
    # Arange
    sides_code = '123abc456def'
    direction = Direction.WEST
    tile = Tile(sides_code=sides_code)
    
    # Act
    code_group = tile.get_code_group(direction)
    
    # Assert
    assert code_group == 'def'

# ==========================================================================

def test_match_sides_code_self_direction_type_error():
    # Arange
    self_direction = 'NORTH'
    other_direction = 'SOUTH'
    tile_self = Tile()
    tile_other = Tile()
    
    # Act
    with pytest.raises(TypeError) as e:
        tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert str(e.value) == 'self_direction must be of type \'Direction\''


def test_match_sides_code_other_direction_type_error():
    # Arange
    self_direction = Direction.NORTH
    other_direction = 'SOUTH'
    tile_self = Tile()
    tile_other = Tile()
    
    # Act
    with pytest.raises(TypeError) as e:
        tile_self.match_sides_code(tile_other, self_direction, other_direction) 
    
    # Assert
    assert str(e.value) == 'other_direction must be of type \'Direction\''


def test_match_sides_code_self_direction_value_error():
    # Arange
    self_direction = Direction.INVALID
    other_direction = Direction.SOUTH
    tile_self = Tile()
    tile_other = Tile()
    
    # Act
    with pytest.raises(ValueError) as e:
        tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert str(e.value) == 'Invalid direction: self_direction'


def test_match_sides_code_other_direction_value_error():
    # Arange
    self_direction = Direction.NORTH
    other_direction = Direction.INVALID
    tile_self = Tile()
    tile_other = Tile()
    
    # Act
    with pytest.raises(ValueError) as e:
        tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert str(e.value) == 'Invalid direction: other_direction'


def test_match_sides_code_true_north_south():
    # Arange
    self_direction = Direction.NORTH
    other_direction = Direction.SOUTH
    tile_self = Tile(sides_code='+++123456789')
    tile_other = Tile(sides_code='123456+++789')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is True


def test_match_sides_code_true_south_north():
    # Arange
    self_direction = Direction.SOUTH
    other_direction = Direction.NORTH
    tile_self = Tile(sides_code='123456+++789')
    tile_other = Tile(sides_code='+++123456789')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is True


def test_match_sides_code_true_east_west():
    # Arange
    self_direction = Direction.EAST
    other_direction = Direction.WEST
    tile_self = Tile(sides_code='123+++456789')
    tile_other = Tile(sides_code='123456789+++')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is True


def test_match_sides_code_true_west_east():
    # Arange
    self_direction = Direction.WEST
    other_direction = Direction.EAST
    tile_self = Tile(sides_code='123456789+++')
    tile_other = Tile(sides_code='123+++456789')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is True


def test_match_sides_code_false_north_south():
    '''
    from tile_self, '111' is taken
    from tile_other, exactly 'aaa' has to be taken so it doesn't match to tile_self
    '''
    # Arange
    self_direction = Direction.NORTH
    other_direction = Direction.SOUTH
    tile_self = Tile(sides_code='111aaaaaaaaa')
    tile_other = Tile(sides_code='111111aaa111')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is False


def test_match_sides_code_false_south_north():
    # Arange
    self_direction = Direction.SOUTH
    other_direction = Direction.NORTH
    tile_self = Tile(sides_code='aaaaaa111aaa')
    tile_other = Tile(sides_code='aaa111111111')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is False


def test_match_sides_code_false_east_west():
    # Arange
    self_direction = Direction.EAST
    other_direction = Direction.WEST
    tile_self = Tile(sides_code='aaa111aaaaaa')
    tile_other = Tile(sides_code='111111111aaa')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is False


def test_match_sides_code_false_west_east():
    # Arange
    self_direction = Direction.WEST
    other_direction = Direction.EAST
    tile_self = Tile(sides_code='aaaaaaaaa111')
    tile_other = Tile(sides_code='111aaa111111')
    
    # Act
    result = tile_self.match_sides_code(tile_other, self_direction, other_direction)
    
    # Assert
    assert result is False
