from pathlib import Path
from PIL import Image
from src.readers.image_reader import read_image, read_images

def test_read_image():
    # Arange
    image_path = Path('tests/resources/black.png')
    
    # Act
    image = read_image(image_path)
    
    # Assert
    assert image is not None
    assert isinstance(image, Image.Image) is True
    assert image.size == (40, 40)


def test_read_images_png():
    # Arange
    dir_path = Path('tests/resources')
    
    # Act
    images = read_images(dir_path)
    
    # Assert
    assert len(images) == 1
    assert 'black' in images


def test_read_images_jpeg_none():
    # Arange
    dir_path = Path('tests/resources')
    
    # Act
    images = read_images(dir_path, file_extension='.jpeg')
    
    # Assert
    assert len(images) == 0
    assert 'black' not in images