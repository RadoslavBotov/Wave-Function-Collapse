import tkinter as tk
from src.cells.cell import Cell
from src.highlight_data import HighlightData
from src.direction import Direction
from src.tiles.tile_set_manager import TileSetManager
from src.tiles.tile import Tile


class CellManager:
    VALID_REDUCE_MOVES = [ 
        (-1,  0, Direction.SOUTH),
        ( 0,  1, Direction.WEST),
        ( 1,  0, Direction.NORTH),
        ( 0, -1, Direction.EAST)
    ]
    
    def __init__(self, rows: int, columns: int, cell_size: int|tuple[int, int], canvas: tk.Canvas, tile_set_manager: TileSetManager):
        self.cells: list[list[Cell]] = []
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.canvas = canvas
        self.tile_set_manager = tile_set_manager
        
        self._current_tile_set = 'default_tile_set'
        self._highlight_data = HighlightData()


    def highlight_cell(self, row: int, column: int) -> None:
        self.cells[row][column].highlight(self._highlight_data)


    def collapse(self, row: int, column: int) -> None|Tile:
        cell = self.cells[row][column]
        chosen_tile = cell.collapse()
        
        if chosen_tile is None:
            return None

        cell.draw(chosen_tile)
        return chosen_tile  


    def reduce_possibilities_for(self, row: int, column: int, chosen_tile: Tile) -> None:
        for i, j, self_dir in CellManager.VALID_REDUCE_MOVES:
            if 0 <= row + i < self.rows and 0 <= column + j < self.columns:
                self.cells[row + i][column + j].reduce_possibilities(chosen_tile, self_dir, self_dir.get_opposite())


    def getCellIndices(self, x: int, y: int) -> tuple[int, int]:
        if self.are_valid_cell_coordinates(x, y) is not True:
            return (-1, -1)
        
        column = x // self.cell_size[0]
        row = y // self.cell_size[1]

        return row, column


    def are_valid_cell_coordinates(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows * self.cell_size[0] and 0 <= column < self.columns * self.cell_size[1]


    def load_cells_with_current_tile_set(self, bool_variable) -> None:
        tile_set = self.tile_set_manager[self._current_tile_set]
        tile_set_image_size = tile_set.get_tile_image_size()
        if tile_set_image_size is None:
            raise ValueError('TileSet with None image.')
        
        for cell_row in self.cells:
            for cell in cell_row:
                cell.clear()
                
        self.cells.clear()
        
        for row in range(self.rows):
            row_of_cells = []
            for column in range(self.columns):
                cell = Cell(row, column, tile_set_image_size, tile_set, self.canvas)
                row_of_cells.append(cell)
                
                if bool_variable.get() is True:
                    cell.enable_extra_information()
                
            self.cells.append(row_of_cells)
    

    def switch_tile_sets_with(self, bool_variable: tk.BooleanVar, new_tile_set='default_tile_set') -> None:
        if new_tile_set not in self.tile_set_manager:
            raise ValueError('Invalid tile set name. No such tile set was loaded. Check for spelling errors in file names or the tile config file.')
        
        self._current_tile_set = new_tile_set
        self.load_cells_with_current_tile_set(bool_variable)


    def save_current_image(self):
        pass
    
    
    def enable_cell_extra_information(self) -> None:
        for cell_list in self.cells:
            for cell in cell_list:
                cell.enable_extra_information()


    def disable_cell_extra_information(self) -> None:
        for cell_list in self.cells:
            for cell in cell_list:
                cell.disable_extra_information()
