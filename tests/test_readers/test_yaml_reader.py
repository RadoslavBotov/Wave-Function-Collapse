from pathlib import Path
from src.readers.yaml_reader import read_config_file

def test_read_config_file_empty():
    # Arrange
    config_path = Path('tests/resources/empty_configs.yaml')
    expected_result = {}
    
    # Act
    result = read_config_file(config_path)
    
    # Assert
    assert result == expected_result


def test_read_config_file_has():
    # Arrange
    config_path = Path('tests/resources/has_configs.yaml')
    expected_result = {'setting1': 'value1', 'setting2': 'value2', 'settings4': {'sub41': 'value4', 'sub42': 'value5'},}

    # Act
    result = read_config_file(config_path)
    
    # Assert
    assert result == expected_result


def test_read_config_file_tile_set_valid():
    # Arrange
    config_path = Path('tests/resources/tile_set_configs.yaml')
    expected_result = {
        'corner': {
            'directions': '100000000001',
            'rotations': 3
            },
        'wall': {
            'directions': '100 000 001 111',
            'rotations': 3
            },
        'blank': {
            'directions': 0
            },
        'fill': {
            'directions': 1
            },
        'check': {
            'directions': '100001100001',
            'rotations': 3
            },
        'three-parts': {
            'directions':{
                'north': 1,
                'east': 1,
                'south': '100',
                'west': '001'
                },
            'rotations': 3
            }
        }
    
    # Act
    result = read_config_file(config_path)
    
    # Assert
    assert result == expected_result
