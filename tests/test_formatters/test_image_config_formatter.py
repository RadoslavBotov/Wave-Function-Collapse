import pytest
from src.exceptions.tile_set_format_error import TileSetFormatError
from src.formatters.image_config_formatter import ( 
        _format_directions_int,
        _format_directions_str,
        _get_correct_directions_order,
        _format_directions_dict,
        _format_directions,
        _format_rotations,
        format_image_configs
    )

# ====================================================================================

def test_format_directions_int_negative():
    # Arange
    directions = -1
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _format_directions_int(directions)
    
    # Assert
    assert str(e.value) == 'Integer directions must be digits [0:9]'


def test_format_directions_int_double_digit():
    # Arange
    directions = 11
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _format_directions_int(directions)
    
    # Assert
    assert str(e.value) == 'Integer directions must be digits [0:9]'
    

def test_format_directions_int_tweve():
    # Arange
    directions = 1
    
    # Act
    result = _format_directions_int(directions)
    
    # Assert
    assert result == '111111111111'


def test_format_directions_int_three():
    # Arange
    directions = 1
    
    # Act
    result = _format_directions_int(directions, 3)
    
    # Assert
    assert result == '111'

# ====================================================================================
    
def test_format_directions_str_invalid_length():
    # Arange
    directions = 'aaa'
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _format_directions_str(directions)
    
    # Assert
    assert str(e.value) == 'Invalid direction string. Must be 12 characters long.'


def test_format_directions_str_twelve():
    # Arange
    directions = 'a'
    
    # Act
    result = _format_directions_str(directions)
    
    # Assert
    assert result == 'aaaaaaaaaaaa'


def test_format_directions_str_three():
    # Arange
    directions = 'a'
    
    # Act
    result = _format_directions_str(directions, 3)
    
    # Assert
    assert result == 'aaa'
    
# ====================================================================================
    
def test_get_correct_directions_order_wrong_key():
    # Arange
    directions = {
        'north': 1,
        'east': 2,
        'south': '3',
        'EEEEEE': '4'
    }
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _get_correct_directions_order(directions)
    
    # Assert
    assert str(e.value) == 'Invalid directions keys. Must be [north|east|south|west]'


def test_get_correct_directions_order_out_of_order():
    # Arange
    directions = {
        'east': 2,
        'west': 4,
        'south': 3,
        'north': 1
    }
    
    # Act
    order = _get_correct_directions_order(directions) # type: ignore
    
    # Assert
    assert order == [1, 2, 3, 4]


def test_get_correct_directions_order_in_order():
    # Arange
    directions = {
        'north': 1,
        'east': 2,
        'south': 3,
        'west': 4,
    }
    
    # Act
    order = _get_correct_directions_order(directions) # type: ignore
    
    # Assert
    assert order == [1, 2, 3, 4]

# ====================================================================================
    
def test_format_directions_dict_incorect_length():
    # Arange
    directions = {
        'north': 1,
        'east': 2,
        'south': 3
    }
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _format_directions_dict(directions)
    
    # Assert
    assert str(e.value) == 'Invalid direction dict. Must be 4 entries.'


def test_format_directions_dict_only_integers():
    # Arange
    directions = {
        'north': 1,
        'east': 2,
        'south': 3,
        'west': 4,
    }
    
    # Act
    result = _format_directions_dict(directions)
    
    # Assert
    assert result == '111222333444'


def test_format_directions_dict_only_strings():
    # Arange
    directions = {
        'north': 'a',
        'east': 'b',
        'south': 'c',
        'west': 'd',
    }
    
    # Act
    result = _format_directions_dict(directions)
    
    # Assert
    assert result == 'aaabbbcccddd'


def test_format_directions_dict_mixed():
    # Arange
    directions = {
        'north': 1,
        'east': 'b',
        'south': 2,
        'west': 'd',
    }
    
    # Act
    result = _format_directions_dict(directions)
    
    # Assert
    assert result == '111bbb222ddd'
    
# ====================================================================================

def test_format_directions_integer():
    # Arange
    directions = 1
    
    # Act
    result = _format_directions(directions)
    
    # Assert
    assert result == '111111111111'


def test_format_directions_string():
    # Arange
    directions = 'a'
    
    # Act
    result = _format_directions(directions)
    
    # Assert
    assert result == 'aaaaaaaaaaaa'


def test_format_directions_dictionary():
    # Arange
    directions = {
        'north': 1,
        'east': 'b',
        'south': 2,
        'west': 'd',
    }
    
    # Act
    result = _format_directions(directions)
    
    # Assert
    assert result == '111bbb222ddd'


def test_format_directions_invalid_format():
    # Arange
    directions = (1, 'b')
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _format_directions(directions)
    
    # Assert
    assert str(e.value) == 'Unknown direction format.'

# ====================================================================================

def test_format_rotations_zero():
    # Arange
    rotations = 0
    
    # Act
    result = _format_rotations(rotations)
    
    # Assert
    assert result == []


def test_format_rotations_one():
    # Arange
    rotations = 1
    
    # Act
    result = _format_rotations(rotations)
    
    # Assert
    assert result == [(1, 'left')]


def test_format_rotations_two():
    # Arange
    rotations = 2
    
    # Act
    result = _format_rotations(rotations)
    
    # Assert
    assert result == [(1, 'left'), (2, 'left')]


def test_format_rotations_invalid_format():
    # Arange
    rotations = 'a'
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        _format_rotations(rotations) # type: ignore
    
    # Assert
    assert str(e.value) == 'Unknown rotations format. Must be an integer.'

# ====================================================================================

def test_format_image_configs_missing_directions():
    # Arange
    configs_unformatted = {
        'corner': { 'directions': '100000000001', 'rotations': 3 },
        'wall': { 'rotations': 3 },
    }
    
    # Act
    with pytest.raises(TileSetFormatError) as e:
        format_image_configs(configs_unformatted)
    
    # Assert
    assert str(e.value) == 'Invalid tile description. Directions are missing.'


def test_format_image_configs():
    # Arange
    configs_unformatted = {
        'corner': { 'directions': '100000000001', 'rotations': 3 },
        'wall': { 'directions': '100 000 001 111', 'rotations': 3 },
        'blank': { 'directions': 0 },
        'fill': { 'directions': 1 },
        'check': { 'directions': '100001100001', 'rotations': 3 },
        'three-parts': { 'directions':{ 'north': 1, 'east': 1, 'south': '100', 'west': '001' }, 'rotations': 3 }
    }
    expected_result = {
        'corner': { 'directions': '100000000001', 'rotations': [(1, 'left'), (2, 'left'), (3, 'left')] },
        'wall': { 'directions': '100000001111', 'rotations': [(1, 'left'), (2, 'left'), (3, 'left')] },
        'blank': { 'directions': '000000000000', 'rotations': [] },
        'fill': { 'directions': '111111111111', 'rotations': [] },
        'check': { 'directions': '100001100001', 'rotations': [(1, 'left'), (2, 'left'), (3, 'left')] },
        'three-parts': { 'directions': '111111100001', 'rotations': [(1, 'left'), (2, 'left'), (3, 'left')] }
    }
    
    # Act
    result = format_image_configs(configs_unformatted)
    
    # Assert
    assert result == expected_result
