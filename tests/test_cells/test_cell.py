from PIL import Image, ImageTk
from src.cells.cell import Cell
from src.constants import ERROR_BACKGROUND_TILE
from src.direction import Direction
from src.tiles.tile import Tile
from src.tiles.tile_set import TileSet


def test_get_coordinates():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = (0, 0)
    
    # Act
    result = cell.get_coordinates()
     
    # Assert
    assert result == expected_result

# =======================================================================

def test_get_tile_set_size_collapsed():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    cell._is_collapsed = True
    expected_result = -1
    
    # Act
    result = cell.get_tile_set_size()
     
    # Assert
    assert result == expected_result


def test_get_tile_set_size_actual():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = 2
    
    # Act
    result = cell.get_tile_set_size()
     
    # Assert
    assert result == expected_result

# ===================================================================

def test_get_chosen_image_default_image():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = Image.new('RGB', (40, 40), color='white')
    
    # Act
    result = cell.get_chosen_image()
     
    # Assert
    assert result == expected_result


def test_get_chosen_image_actual_image():
    # Arrange
    t1 = Tile(Image.new('RGB', (20, 20), color='red'))
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    cell._is_collapsed = True
    cell._chosen_tile = t1
    expected_result = Image.new('RGB', (20, 20), color='red')
    
    # Act
    result = cell.get_chosen_image()
     
    # Assert
    assert result == expected_result

# ==============================================================================

def test_resize_cell_no_resize():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = False
    
    # Act
    result = cell.resize_cell((20, 20))
     
    # Assert
    assert result == expected_result
    assert cell.cell_size == (40, 40)
    assert cell._chosen_tile is None
    assert t1.image is None
    assert t2.image is None


def test_resize_cell_no_chosen_tile():
    # Arrange
    t1 = Tile(Image.new('RGB', (40, 40), color='red'))
    t2 = Tile(Image.new('RGB', (40, 40), color='red'))
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = True
    
    # Act
    result = cell.resize_cell((20, 20))
     
    # Assert
    assert result == expected_result
    assert cell._chosen_tile is None
    assert cell.cell_size == (20, 20)
    assert t1.image.size == (20, 20)
    assert t2.image.size == (20, 20)


def test_resize_cell_chosen_tile():
    # Arrange
    t1 = Tile(Image.new('RGB', (40, 40), color='red'))
    t2 = Tile(Image.new('RGB', (40, 40), color='red'))
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    cell._chosen_tile = t1
    expected_result = True
    
    # Act
    result = cell.resize_cell((20, 20))
     
    # Assert
    assert result == expected_result
    assert cell._chosen_tile == t1
    assert cell.cell_size == (20, 20)
    assert t1.image.size == (20, 20)
    assert t2.image.size == (40, 40)

# ==============================================================================

def test_collapse_already_collapsed():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    cell._is_collapsed = True
    expected_result = None
    
    # Act
    result = cell.collapse()
     
    # Assert
    assert result == expected_result


def test_collapse_valid_cell():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = set([t1, t2])
    
    # Act
    result = cell.collapse()
     
    # Assert
    assert result in expected_result


def test_collapse_invalid_cell_default_size():
    # Arrange
    tile_set = TileSet()
    cell = Cell(0, 0, (40, 40), tile_set)
    expected_result = ERROR_BACKGROUND_TILE
    
    # Act
    result = cell.collapse()
     
    # Assert
    assert result == expected_result
    assert expected_result.image.size == (40, 40)


def test_collapse_invalid_cell_different_size():
    # Arrange
    tile_set = TileSet()
    cell = Cell(0, 0, (20, 20), tile_set)
    expected_result = ERROR_BACKGROUND_TILE
    
    # Act
    result = cell.collapse()
     
    # Assert
    assert result == expected_result
    assert expected_result.image.size == (20, 20)

# ======================================================================

def test_reduce_tile_set_already_collapsed():
    # Arrange
    t1 = Tile()
    t2 = Tile()
    t3 = Tile()
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (20, 20), tile_set)
    cell._is_collapsed = True
    expected_result = None
    
    # Act
    result = cell.reduce_tile_set(t3, Direction.NORTH, Direction.SOUTH)
     
    # Assert
    assert result == expected_result


def test_reduce_tile_set_no_removed():
    # Arrange             [N][E][S][W]
    t1 = Tile(sides_code='+++***++++++')
    t2 = Tile(sides_code='++++++***+++')
    t3 = Tile(sides_code='+++++++++***')
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (20, 20), tile_set)
    expected_result = 2
    
    # Act
    result = cell.reduce_tile_set(t3, Direction.NORTH, Direction.SOUTH)
     
    # Assert
    assert result == expected_result


def test_reduce_tile_set_all_removed():
    # Arrange             [N][E][S][W]
    t1 = Tile(sides_code='+++***++++++')
    t2 = Tile(sides_code='+++++++++***')
    t3 = Tile(sides_code='++++++***+++')
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (20, 20), tile_set)
    expected_result = 0
    
    # Act
    result = cell.reduce_tile_set(t3, Direction.NORTH, Direction.SOUTH)
     
    # Assert
    assert result == expected_result


def test_reduce_tile_set_one_removed():
    # Arrange             [N][E][S][W]
    t1 = Tile(sides_code='+++***++++++')
    t2 = Tile(sides_code='+++++++++***')
    t3 = Tile(sides_code='++++++***+++')
    tile_set = TileSet([t1, t2])
    cell = Cell(0, 0, (20, 20), tile_set)
    expected_result = 1
    
    # Act
    result = cell.reduce_tile_set(t3, Direction.EAST, Direction.WEST)
     
    # Assert
    assert result == expected_result

### =============================================================
# Other methods were not tested because of tk.Canvas dependency:
# - draw(), clear(), highlight()
# - update_extra_information()
# - enable_extra_information()
# - disable-extra_information()
### =============================================================
