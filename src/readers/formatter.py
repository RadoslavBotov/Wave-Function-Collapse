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
            formatted_configs[image_name]['directions'] = (-1, -1, -1, -1)
            return

        if isinstance(directions, dict):
            directions_tuple = cls.__get_correct_direction_order(directions)
            formatted_configs[image_name]['directions'] = directions_tuple


    @classmethod
    def __get_correct_direction_order(cls, directions: dict[str, int]) -> tuple[int, int, int, int]:
        '''
        
        '''
        return (directions['north'], directions['east'], directions['south'], directions['west'])


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
