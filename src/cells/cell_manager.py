from tkinter import Canvas
from src.cells.cell import Cell
from src.cells.highlight_data import HighlightData
from src.cells.direction import Direction
from src.tiles.tile_set_manager import TileSetManager


class CellManager:
    MOVES = [(-1, 0, Direction.NORTH), (0, 1, Direction.EAST), (1, 0, Direction.SOUTH), (0, -1, Direction.WEST)]
    
    def __init__(self, rows: int, columns: int, cell_size: int, canvas: Canvas, tile_set_manager: TileSetManager):
        self.cells: list[list[Cell]] = []
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.canvas = canvas
        self.tile_set_manager = tile_set_manager
        
        self._current_tile_set = 'default_tile_set'
        self._highlight_data = HighlightData()


    def highlight_cell(self, x, y):
        row, column = self.getCellIndex(x, y)
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.cells[row][column].highlight(self._highlight_data)


    def collapse(self, x, y):
        row, column = self.getCellIndex(x, y)
        cell = self.cells[row][column]
        cell.collapse()

        for i, j, dir in CellManager.MOVES:
            if 0 <= row + i < self.rows and 0 <= column + j < self.columns:
                self.cells[row + i][column + j].reduce_possibilities(cell, dir)


    def getCellIndex(self, x, y):
        column = x // self.cell_size
        row = y // self.cell_size

        return row, column

    
    def load_cells_with_current_tile_set(self):
        
        tile_set = self.tile_set_manager[self._current_tile_set]
        tile_set_image_size = tile_set.get_tile_image_size()
        if tile_set_image_size is None:
            raise ValueError('TileSet with None image.')
        
        self.cells.clear()
        
        for row in range(self.rows):
            row_of_cells = []
            for column in range(self.columns):
                row_of_cells.append(Cell(row, column, tile_set_image_size, self.canvas, possibilities=tile_set))
                
            self.cells.append(row_of_cells)
    

    def switch_tile_sets_with(self, new_tile_set='default_tile_set'):
        if new_tile_set not in self.tile_set_manager:
            raise ValueError('Invalid tile set name. No such tile set was loaded. Check for spelling errors in file names or the tile config file.')
        
        self._current_tile_set = new_tile_set
        self.load_cells_with_current_tile_set()


    def save_current_image(self):
        pass
