"""
Gives functionality to read *.yaml files and images(directory with image files[png or jpeg]).
"""

import os

import yaml

from PIL import Image


def read_config_file(file_path: str) -> dict[str, str|int]:
    '''
    Reads a *.yaml file and returns its dict representation.
    - file_path - qwe
    '''
    with open(file_path, "r") as f:
        loaded_configs = yaml.load(f, Loader=yaml.CLoader)
        return loaded_configs


def read_images(directory_path: str, file_extension: str = '.png') -> dict[str, Image.Image]:
        '''
        Reads all image files with @file_extension in specified @directory_path and
        returns a dict in format {image_name: Image}.
        '''
        return {
            file_name[:-len(file_extension)]: Image.open(os.path.join(directory_path, file_name), 'r')
            for file_name
            in [f for f in os.listdir(directory_path) if f.endswith(file_extension)]
        }
