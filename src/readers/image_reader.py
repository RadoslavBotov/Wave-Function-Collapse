"""
Gives functionality to read images(directory with image files[png or jpeg]).
"""

from pathlib import Path

from PIL import Image


def read_images(directory_path: Path, file_extension: str = '.png') -> dict[str, Image.Image]:
    '''
    Opens all image files with @file_extension in specified @directory_path.
    
    Returns a dict of {'image_name': PIL.Image}.
    
    - directory_path - Path of directory from which images are read
    - file_extension - only images with this extension are opened
    '''
    return {
        image_path.stem: read_image(directory_path / image_path.name)
        for image_path
        in directory_path.glob('*' + file_extension)
    }


def read_image(image_file_path: Path) -> Image.Image:
    '''
    Tries to open a PIL.Image file from given path.
    
    If file exists and is in a format PIL can read, returns an Image.
    
    - image_file_path - Path of image file
    '''
    return Image.open(image_file_path, 'r')
