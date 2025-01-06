from src.exceptions.tile_set_format_error import TileSetFormatError
from src.formatters.base_formatter import Formatter


class ConfigFormatter(Formatter):
    @classmethod
    def format_item(cls, configs: dict) -> dict:
        formatted_configs = configs.copy()

        for image_name in configs:
            try:
                directions = configs[image_name]['directions']
                formatted_configs[image_name]['directions'] = cls.__format_directions(directions)
            except KeyError:
                raise TileSetFormatError('Invalid tile description. Directions are missing, but are mandatory.')
            
            try:
                rotations = formatted_configs[image_name]['rotations']
                formatted_configs[image_name]['rotations'] = cls._format_rotations(rotations)
            except KeyError:
                formatted_configs[image_name]['rotations'] = []

        return formatted_configs


    @classmethod
    def __format_directions(cls, directions) -> str:
        if isinstance(directions, int):
            return str(directions) * 12
        
        if isinstance(directions, str):
            directions = directions.replace(' ', '')
            if len(directions) == 1:
                return directions * 12
            
            if len(directions) != 12:
                raise TileSetFormatError('Invalid direction string. Must be 12 characters long.')
            
            return directions
        
        if isinstance(directions, dict):
            if len(directions) != 4:
                raise TileSetFormatError('Invalid direction dict. Less/More than 4 entries.')
            
            correct_order = cls.__get_directions_in_correct_order(directions)
            correct_directions = [cls.__get_correct_direction_format(x) for x in correct_order]
            return ''.join(correct_directions)

        raise TileSetFormatError('Unknown direction format.')


    @classmethod
    def __get_directions_in_correct_order(cls, directions: dict[str, int|str]) -> list[int|str]:
        try:
            correct_order = [directions['north'], directions['east'], directions['south'], directions['west']]
        except KeyError:
            raise TileSetFormatError('Invalid directions key names. Must be [north|east|south|west].')
        
        return correct_order


    @classmethod
    def __get_correct_direction_format(cls, direction: int|str) -> str:
        if isinstance(direction, int):
            return str(direction) * 3
        
        if isinstance(direction, str):
            if len(direction) == 1:
                return direction * 3
            
            if len(direction) != 3:
                raise TileSetFormatError(f'Invalid direction: {direction}. Length must be 1, 3, or an integer')
            
            return direction

        raise TileSetFormatError('Unknown direction format.')


    @classmethod
    def _format_rotations(cls, rotations: int):
        if isinstance(rotations, int):
            formatted_rotations = [
                (item, 'left')
                for item
                in range(1, rotations+1)
            ]
            
            return formatted_rotations

        raise TileSetFormatError('Unknown rotations format. Must be an integer.')
