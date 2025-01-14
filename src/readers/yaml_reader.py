'''
Gives functionality to read yaml files.
'''
from pathlib import Path

import yaml


def read_config_file(yaml_file_path: Path) -> dict[str, str|int]:
    '''
    Opens a *.yaml file and returns its dict representation.

    - yaml_file_path - Path of yaml file to open
    '''
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        loaded_configs = yaml.load(f, Loader=yaml.CLoader)
        return loaded_configs
