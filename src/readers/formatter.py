class ConfigFormatter:
    @classmethod
    def format_configs_for_images(cls, configs: dict) -> dict:
        formatted_configs = configs.copy()

        for image_name in formatted_configs:
            cls.__format_directions(formatted_configs, image_name)
            cls.__format_rotations(formatted_configs, image_name)

        return formatted_configs


    @classmethod
    def __format_directions(cls, formatted_configs, image_name):
        try:
            directions = formatted_configs[image_name]['directions']
        except KeyError:
            formatted_configs[image_name]['directions'] = ('---', '---', '---', '---')
            return
        
        if isinstance(directions, str):
            if len(directions) != 12:
                raise ValueError('Invalid direction string. Must be 12 characters long')
            
            return directions
        
        if isinstance(directions, dict):
            directions_tuple = cls.__get_correct_direction_order(directions)
            formatted_configs[image_name]['directions'] = directions_tuple


    @classmethod
    def __get_correct_direction_order(cls, directions: dict[str, int]) -> str:
        '''
        
        '''
        correct_order = [
            cls.__get_correct_direction_format(directions['north']),
            cls.__get_correct_direction_format(directions['east']),
            cls.__get_correct_direction_format(directions['south']),
            cls.__get_correct_direction_format( directions['west'])
        ]
        
        return ''.join(correct_order)
        


    @classmethod
    def __get_correct_direction_format(cls, direction: int|str) -> str:
        if isinstance(direction, int):
            return f'{direction}{direction}{direction}'
        
        if isinstance(direction, str):
            if len(direction) != 3:
                raise ValueError(f'Invalid direction: {direction}. Length must be 3, or an integer')
            
            return direction


    @classmethod
    def __format_rotations(cls, formatted_configs, image_name):
        try:
            rotations = formatted_configs[image_name]['rotations']
        except KeyError:
            formatted_configs[image_name]['rotations'] = []
            return

        if isinstance(rotations, int):
            formatted_rotations = [
                item
                for command
                in range(1, rotations+1)
                    for item
                    in cls.__format_rotation_commands(f'{command}-left')
            ]
            
            formatted_configs[image_name]['rotations'] = formatted_rotations

        if isinstance(rotations, list):
            formatted_rotations = [
                item
                for command
                in rotations
                    for item
                    in cls.__format_rotation_commands(command)
            ]

            # flatten formatted_rotations from list[list[tuple]] to list[tuple]
            formatted_configs[image_name]['rotations'] = formatted_rotations
            return


    @classmethod
    def __format_rotation_commands(cls, command: str) -> list[tuple[int, str]]:
        rotation_amounts, rotation_direction = command.split('-')

        return [(int(a.strip()), rotation_direction) for a in rotation_amounts.split(',')]
