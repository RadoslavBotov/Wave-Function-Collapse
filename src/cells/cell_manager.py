'''
CellManager
'''
import tkinter as tk
from PIL import Image
from src.constants import VALID_REDUCE_MOVES
from src.cells.cell import Cell
from src.highlight_data import HighlightData
from src.tiles.tile_set_manager import TileSetManager
from src.tiles.tile import Tile


class CellManager:
    '''
    Provides methods to manage a cell grid.
    '''
    def __init__(self,
                 rows: int,
                 columns: int,
                 cell_size: int|tuple[int, int],
                 canvas: tk.Canvas,
                 tile_set_manager: TileSetManager) -> None:
        self.cells: list[list[Cell]] = []
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size if isinstance(cell_size, tuple) else (cell_size, cell_size)
        self.canvas = canvas
        self.tile_set_manager = tile_set_manager

        self._current_tile_set = 'default_tile_set'
        self._highlight_data = HighlightData()


    def highlight_cell(self, row: int, column: int) -> None:
        '''
        Highlights(draw a rectangle) the given cell if it wasn't the last highlighted cell.
        Otherwise, does nothing.
        '''
        self.cells[row][column].highlight(self._highlight_data, self.canvas)


    def collapse(self, row: int, column: int) -> None|Tile:
        '''
        Collapses given cell, chasing a random tile that satisfies surrounding constraints
        and draws that tile to canvas.
        '''
        cell = self.cells[row][column]
        chosen_tile = cell.collapse()

        if chosen_tile is None:
            return None

        cell.draw(chosen_tile, self.canvas)
        return chosen_tile


    def reduce_possibilities_for(self, row: int, column: int, chosen_tile: Tile) -> None:
        '''
        When a cell is collapsed, this method should be invoked on that cell.
        Reduces the neighboring cells' tilesets, according to 
        the constraints(sides_code) of the chosen_tile.
        '''
        for i, j, self_dir in VALID_REDUCE_MOVES:
            if 0 <= row + i < self.rows and 0 <= column + j < self.columns:
                cell = self.cells[row + i][column + j]
                new_tile_set_size = cell.reduce_tile_set(chosen_tile, self_dir,
                                                         self_dir.get_opposite())
                cell.update_extra_information(self.canvas, new_tile_set_size)


    def get_cell_indices(self, x: int, y: int) -> tuple[int, int]:
        '''
        Accepts pixel coordinates from a canvas(or other) and
        translates them to coordinates in the cell grid.
        
        Let X = rows * cell_size and Y = columns * cell_size.
        Then x in [0, X] and y in [0, Y]. Grid coordinates are
        in ranges [0, rows], [0, columns].
        '''
        if self.are_valid_cell_coordinates(x, y) is not True:
            return (-1, -1)

        column = x // self.cell_size[0] # horizontal axis for column index
        row = y // self.cell_size[1] # vertical axis for row index

        return row, column


    def are_valid_cell_coordinates(self, x: int, y: int) -> bool:
        '''
        Returns true if pixel coordinates are in valid range.
        Let X = rows * cell_size and Y = columns * cell_size.
        Then x in [0, X] and y in [0, Y].
        '''
        return 0 <= x < self.rows * self.cell_size[0] and 0 <= y < self.columns * self.cell_size[1]


    def load_cells_with_current_tile_set(self, bool_variable) -> None:
        '''
        
        '''
        tile_set = self.tile_set_manager[self._current_tile_set]
        tile_set_image_size = tile_set.get_tile_image_size()
        if tile_set_image_size is None:
            raise ValueError('TileSet with None image.')

        for cell_row in self.cells:
            for cell in cell_row:
                cell.clear(self.canvas)

        self.cells.clear()

        for row in range(self.rows):
            row_of_cells = []
            for column in range(self.columns):
                cell = Cell(row, column, tile_set_image_size, tile_set)
                row_of_cells.append(cell)

                if bool_variable.get() is True:
                    cell.enable_extra_information(self.canvas)

            self.cells.append(row_of_cells)


    def switch_tile_sets_with(self,
                              bool_variable: tk.BooleanVar,
                              new_tile_set='default_tile_set') -> None:
        '''
        
        '''
        if new_tile_set not in self.tile_set_manager:
            raise ValueError('Invalid tile set name.'
                             'No such tile set was loaded.'
                             'Check for spelling errors in file names or the tile config file.')

        self._current_tile_set = new_tile_set
        self.load_cells_with_current_tile_set(bool_variable)


    def get_current_image(self, background_color: str = 'white') -> Image.Image:
        '''
        Constructs an Image, with size of Canvas, combining all Cell images.
        If some Cell does not have an Image, a default image
        with @background_color is filled in it's place.
        '''
        save_image = Image.new('RGB', (self.canvas.winfo_width(), self.canvas.winfo_height()))

        for cell_row in self.cells:
            for cell in cell_row:
                cell_image = cell.get_chosen_image(background_color)
                save_image.paste(cell_image, (cell.column * cell.cell_size[0],
                                              cell.row * cell.cell_size[1],))

        return save_image


    def enable_cell_extra_information(self) -> None:
        '''
        Show number of tile's in a cells tilesets on canvas.
        '''
        for cell_list in self.cells:
            for cell in cell_list:
                cell.enable_extra_information(self.canvas)


    def disable_cell_extra_information(self) -> None:
        '''
        Remove number of tile's in a cells tilesets on canvas.
        '''
        for cell_list in self.cells:
            for cell in cell_list:
                cell.disable_extra_information(self.canvas)
