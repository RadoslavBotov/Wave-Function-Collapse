from PIL import Image
from src.tiles.tile_set_manager import TileSetManager
from src.tiles.tile_set import TileSet
from src.tiles.tile import Tile

# ==========================================================================

def test_get_tile_set_image_size_empty_manager():
    # Arange
    tsm = TileSetManager()
    
    # Act
    size = tsm.get_tile_set_image_size('invalid_tile_set')
    
    # Assert
    assert size is None


def test_get_tile_set_image_size_empty_tile_set():
    # Arange
    tsm = TileSetManager([('tile_set_name', TileSet())])
    
    # Act
    size = tsm.get_tile_set_image_size('tile_set_name')
    
    # Assert
    assert size is None
    

def test_get_tile_set_image_size_not_in_manager():
    # Arange
    tsm = TileSetManager([('tile_set_name', TileSet())])
    
    # Act
    size = tsm.get_tile_set_image_size('invalid_tile_set')
    
    # Assert
    assert size is None


def test_get_tile_set_image_size_tile():
    # Arange
    tsm = TileSetManager([('tile_set_name', TileSet([Tile(Image.new('RGB', (40, 40)))]))])
    
    # Act
    size = tsm.get_tile_set_image_size('tile_set_name')
    
    # Assert
    assert size == (40, 40)

# ==========================================================================

def test_resize_tile_set_empty_manager():
    # Arange
    tsm = TileSetManager()
    
    # Act
    result = tsm.resize_tile_set('tile_set_name', (40, 80))
    
    # Assert
    assert result is None


def test_resize_tile_set_empty_tile_set():
    # Arange
    tsm = TileSetManager([('tile_set_name', TileSet())])
    
    # Act
    result = tsm.resize_tile_set('tile_set_name', (40, 80))
    
    # Assert
    assert result is False
    

def test_resize_tile_set_not_in_manager():
    # Arange
    tsm = TileSetManager([('tile_set_name', TileSet())])
    
    # Act
    result = tsm.resize_tile_set('invalid', (40, 80))
    
    # Assert
    assert result is None


def test_resize_tile_set_tile():
    # Arange
    tsm = TileSetManager([('tile_set_name', TileSet([Tile(Image.new('RGB', (40, 40)))]))])
    
    # Act
    result = tsm.resize_tile_set('tile_set_name', (40, 80))
    size = tsm.get_tile_set_image_size('tile_set_name')
    
    # Assert
    assert result is True
    assert size == (40, 80)
