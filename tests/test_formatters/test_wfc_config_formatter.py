import pytest
from src.formatters.wfc_config_formatter import _format_cell_size, format_wfc_configs


def test_format_cell_size_invalid():
    # Arrange
    cell_size = 'qwe'
    
    # Act
    with pytest.raises(ValueError) as e:
        result = _format_cell_size(cell_size)
    
    # Assert
    assert str(e.value) == 'Invalid default_cell_size format.'


def test_format_cell_size_int():
    # Arrange
    cell_size = 40
    expected_result = (40, 40)
    
    # Act
    result = _format_cell_size(cell_size)
    
    # Assert
    assert result == expected_result


def test_format_cell_size_tuple():
    # Arrange
    cell_size = (40, 40)
    expected_result = (40, 40)
    
    # Act
    result = _format_cell_size(cell_size)
    
    # Assert
    assert result == expected_result

# ==========================================================================

def test_format_wfc_configs_int():
    # Arrange
    configs = {
        'default_cell_rows': 20,
        'default_cell_columns': 20,
        'default_cell_size': 20,
        'default_tile_path': 'tilesets',
        'default_tile_set': 'basic_tiles_with_rotations',
        'default_solver_delay': 0.01,
    }
    expected_result = {
        'default_cell_rows': 20,
        'default_cell_columns': 20,
        'default_cell_size': (20, 20),
        'default_tile_path': 'tilesets',
        'default_tile_set': 'basic_tiles_with_rotations',
        'default_solver_delay': 0.01,
    }
    
    # Act
    result = format_wfc_configs(configs)
    
    # Assert
    assert result == expected_result


def test_format_wfc_configs_tuple():
    # Arrange
    configs = {
        'default_cell_rows': 20,
        'default_cell_columns': 20,
        'default_cell_size': (20, 20),
        'default_tile_path': 'tilesets',
        'default_tile_set': 'basic_tiles_with_rotations',
        'default_solver_delay': 0.01,
    }
    expected_result = {
        'default_cell_rows': 20,
        'default_cell_columns': 20,
        'default_cell_size': (20, 20),
        'default_tile_path': 'tilesets',
        'default_tile_set': 'basic_tiles_with_rotations',
        'default_solver_delay': 0.01,
    }
    
    # Act
    result = format_wfc_configs(configs)
    
    # Assert
    assert result == expected_result
