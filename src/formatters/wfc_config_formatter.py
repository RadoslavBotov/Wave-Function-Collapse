'''
Formats configs for main program
'''
import copy


def format_wfc_configs(configs: dict) -> dict:
    '''
    Formats main configurations of WFC program.
    '''
    formatted_configs = copy.deepcopy(configs)

    cell_size = formatted_configs['default_cell_size']
    formatted_configs['default_cell_size'] = _format_cell_size(cell_size)

    return formatted_configs


def _format_cell_size(cell_size: int|tuple[int, int]|list[int]) -> tuple[int, int]:
    '''
    Formats default cell size to be a tuple[int, int]
    '''
    if isinstance(cell_size, int):
        return (cell_size, cell_size)

    if isinstance(cell_size, list):
        return cell_size[0], cell_size[1]

    if isinstance(cell_size, tuple):
        return cell_size

    raise ValueError('Invalid default_cell_size format.')
