import tkinter as tk
from PIL import Image
from src.cells.cell_manager import CellManager
from src.solver.solver import Solver
from src.tiles.tile import Tile
from src.tiles.tile_set import TileSet
from src.tiles.tile_set_manager import TileSetManager

ROOT = tk.Tk()
CANVAS = tk.Canvas(ROOT)

# ======================================================================================

def test_get_cells():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = '[<row=0,column=0,tile_set_size=4>, <row=0,column=1,tile_set_size=4>, <row=1,column=0,tile_set_size=4>, <row=1,column=1,tile_set_size=4>]'
    
    # Act
    result = solver._get_cells()
    
    # Assert
    assert str(result) == expected_result

# =======================================================================================

def test_get_min_cells_all():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = '[<row=0,column=0,tile_set_size=4>, <row=0,column=1,tile_set_size=4>, <row=1,column=0,tile_set_size=4>, <row=1,column=1,tile_set_size=4>]'
    
    # Act
    cells = solver._get_cells()
    result = solver.get_min_cells(cells)
    
    # Assert
    assert str(result) == expected_result


def test_get_min_cells_collapsed():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = '[<row=0,column=0,tile_set_size=-1>]'
    
    # Act
    cell_manager.collapse(0, 0)
    cells = solver._get_cells()
    result = solver.get_min_cells(cells)
    
    # Assert
    assert str(result) == expected_result

# =======================================================================================

def test_get_min_cells_score_all():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = 4
    
    # Act
    cells = solver._get_cells()
    result = solver._get_min_cells_score(cells)
    
    # Assert
    assert result == expected_result


def test_get_min_cells_score_collapsed():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = -1
    
    # Act
    cell_manager.collapse(0, 0)
    cells = solver._get_cells()
    result = solver._get_min_cells_score(cells)
    
    # Assert
    assert result == expected_result

# =======================================================================================

def test_prune_collapsed_cells_none():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = '[<row=0,column=0,tile_set_size=4>, <row=0,column=1,tile_set_size=4>, <row=1,column=0,tile_set_size=4>, <row=1,column=1,tile_set_size=4>]'
    
    # Act
    cells = solver._get_cells()
    result = solver._prune_collapsed_cells(cells)
    
    # Assert
    assert str(result) == expected_result


def test_prune_collapsed_cells_one():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = '[<row=0,column=1,tile_set_size=4>, <row=1,column=0,tile_set_size=4>, <row=1,column=1,tile_set_size=4>]'
    
    # Act
    cell_manager.collapse(0, 0)
    cells = solver._get_cells()
    result = solver._prune_collapsed_cells(cells)
    
    # Assert
    assert str(result) == expected_result


def test_prune_collapsed_cells_two():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = '[<row=0,column=1,tile_set_size=4>, <row=1,column=0,tile_set_size=4>]'
    
    # Act
    cell_manager.collapse(0, 0)
    cell_manager.collapse(1, 1)
    cells = solver._get_cells()
    result = solver._prune_collapsed_cells(cells)
    
    # Assert
    assert str(result) == expected_result


def test_prune_collapsed_cells_tall():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    expected_result = []
    
    # Act
    cell_manager.collapse(0, 0)
    cell_manager.collapse(0, 1)
    cell_manager.collapse(1, 0)
    cell_manager.collapse(1, 1)
    cells = solver._get_cells()
    result = solver._prune_collapsed_cells(cells)
    
    # Assert
    assert result == expected_result

# ===================================================================

def test_check_invalid_none_collapsed():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    
    # Act
    solver.check_invalid()
    
    # Assert
    assert cell_manager.cells[0][0]._is_collapsed is False
    assert cell_manager.cells[0][1]._is_collapsed is False
    assert cell_manager.cells[1][0]._is_collapsed is False
    assert cell_manager.cells[1][1]._is_collapsed is False


def test_check_invalid_all_collapsed():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    
    # Act
    cell_manager.collapse(0, 0)
    cell_manager.collapse(0, 1)
    cell_manager.collapse(1, 0)
    cell_manager.collapse(1, 1)
    solver.check_invalid()
    
    # Assert
    assert cell_manager.cells[0][0]._is_collapsed is True
    assert cell_manager.cells[0][1]._is_collapsed is True
    assert cell_manager.cells[1][0]._is_collapsed is True
    assert cell_manager.cells[1][1]._is_collapsed is True


def test_check_invalid_one_invalid():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    
    # Act
    prev_collapsed = cell_manager.cells[0][0]._is_collapsed
    cell_manager.cells[0][0].tile_set = TileSet()
    solver.check_invalid()
    
    # Assert
    assert prev_collapsed is False
    assert cell_manager.cells[0][0]._is_collapsed is True
    assert cell_manager.cells[0][1]._is_collapsed is False
    assert cell_manager.cells[1][0]._is_collapsed is False
    assert cell_manager.cells[1][1]._is_collapsed is False

# =========================================================================

def test_start_has_cells():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    
    # Act
    cell_1_prev_collapsed = cell_manager.cells[0][0]._is_collapsed
    cell_2_prev_collapsed = cell_manager.cells[0][1]._is_collapsed
    cell_3_prev_collapsed = cell_manager.cells[1][0]._is_collapsed
    cell_4_prev_collapsed = cell_manager.cells[1][1]._is_collapsed
    solver.start(False)
    
    # Assert
    assert cell_1_prev_collapsed is False
    assert cell_2_prev_collapsed is False
    assert cell_3_prev_collapsed is False
    assert cell_4_prev_collapsed is False
    assert cell_manager.cells[0][0]._is_collapsed is True
    assert cell_manager.cells[0][1]._is_collapsed is True
    assert cell_manager.cells[1][0]._is_collapsed is True
    assert cell_manager.cells[1][1]._is_collapsed is True


def test_start_no_cells():
    # Arrange
    t1 = Tile(image=Image.new('RGB', (40, 40)), sides_code='111000000000')
    t2 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000000111')
    t3 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000000111000')
    t4 = Tile(image=Image.new('RGB', (40, 40)), sides_code='000111000000')
    tile_set = TileSet([t1, t2, t3, t4])
    tile_set_manager = TileSetManager({'default_tile_set': tile_set})
    cell_manager = CellManager(2, 2, (40, 40), CANVAS, tile_set_manager)
    cell_manager.switch_tile_sets_with(tk.BooleanVar(ROOT, False))
    solver = Solver(cell_manager)
    
    # Act
    cell_manager.cells[0][0]._is_collapsed = True
    cell_manager.cells[0][1]._is_collapsed = True
    cell_manager.cells[1][0]._is_collapsed = True
    cell_manager.cells[1][1]._is_collapsed = True
    solver.start(False)
    
    # Assert
    assert cell_manager.cells[0][0]._is_collapsed is True
    assert cell_manager.cells[0][1]._is_collapsed is True
    assert cell_manager.cells[1][0]._is_collapsed is True
    assert cell_manager.cells[1][1]._is_collapsed is True
