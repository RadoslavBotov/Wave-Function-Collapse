'''
Formats tile set image configurations.
'''
import copy
from src.exceptions.tile_set_format_error import TileSetFormatError


def format_image_configs(configs: dict) -> dict:
    '''
    Formats tile set image configurations to standardize configs.
    The yaml configuration files are in a more human
    readable format, making it easier to write.
    '''
    formatted_configs = copy.deepcopy(configs)

    for image_name in configs:
        try:
            directions = configs[image_name]['directions']
            formatted_configs[image_name]['directions'] = _format_directions(directions)
        except KeyError as e:
            raise TileSetFormatError('Invalid tile description. Directions are missing.') from e

        try:
            rotations = formatted_configs[image_name]['rotations']
            formatted_configs[image_name]['rotations'] = _format_rotations(rotations)
        except KeyError:
            formatted_configs[image_name]['rotations'] = []

    return formatted_configs


def _format_directions(directions, k: int = 12) -> str:
    '''
    Formats direction into a K long character string
    for a Tile sides_code.
    '''
    if isinstance(directions, int):
        return _format_directions_int(directions, k)

    if isinstance(directions, str):
        return _format_directions_str(directions, k)

    if isinstance(directions, dict):
        return _format_directions_dict(directions)

    raise TileSetFormatError('Unknown direction format.')


def _format_directions_int(directions: int, k: int = 12) -> str:
    '''
    Formats integer digit into a K long character string.
    
    - 1 -> '111111111111'
    - 5 -> '555555555555'
    '''
    if directions < 0 or directions > 9:
        raise TileSetFormatError('Integer directions must be digits [0:9]')

    return str(directions) * k


def _format_directions_str(directions: str, k: int = 12) -> str:
    '''
    Formats string into a K long character string.
    All spaces ' ' are replaced with ''.
    
    + directions - must be a string of len of 1 or 12
    
    - 'a' -> 'aaaaaaaaaaaa'
    - '+' -> '++++++++++++'
    '''
    directions = directions.replace(' ', '')

    if len(directions) == 1:
        return directions * k

    if len(directions) != k:
        raise TileSetFormatError('Invalid direction string. Must be 12 characters long.')

    return directions


def _format_directions_dict(directions: dict) -> str:
    '''
    Formats dict into a K character string.
    
    - 'directions': -> '111222333444'
      - 'north': 1
      - 'east': 2
      - 'south': 3
      - 'west': 4
    '''
    if len(directions) != 4:
        raise TileSetFormatError('Invalid direction dict. Must be 4 entries.')

    correct_order = _get_correct_directions_order(directions)
    correct_directions = [_format_directions(x, 3) for x in correct_order]
    return ''.join(correct_directions)


def _get_correct_directions_order(directions: dict[str, int|str]) -> list[int|str]:
    '''
    Accepts a dict with four keys ['north', 'east', 'south', 'west']
    and returns a list with their values in order of
    NORTH, EAST, SOUTH, WEST.
    '''
    try:
        correct_order = [
            directions['north'],
            directions['east'],
            directions['south'],
            directions['west']
        ]
        return correct_order
    except KeyError as e:
        raise TileSetFormatError('Invalid directions keys. Must be [north|east|south|west]') from e


def _format_rotations(rotations: int) -> list[tuple[int , str]]:
    '''
    Accepts an integer rotations and returns a list of tuples:
    [(amount_of_rotations, rotation_direction)]
    
    - rotations: 3 -> [(1, 'left'), (2, 'left'), (3, 'left')]
    '''
    if isinstance(rotations, int):
        formatted_rotations = [
            (item, 'left')
            for item
            in range(1, rotations+1)
        ]

        return formatted_rotations

    raise TileSetFormatError('Unknown rotations format. Must be an integer.')
