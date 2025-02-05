'''
Solver class to automatically fill in grid cell. 
'''
import random
from time import sleep

from src.cells.cell import Cell
from src.cells.cell_manager import CellManager


class Solver:
    '''
    Constraint Satisfaction Problem Solver
    '''
    def __init__(self, cell_manager: CellManager, delay = 0.1) -> None:
        self.cell_manager = cell_manager
        self.delay = delay


    def start(self, update_canvas: bool = True) -> None:
        '''
        Solves the Constraint Satisfaction Problem of choosing appropriate tiles
        for each cell in grid.
        '''
        cells = self._get_cells()
        cells = self._prune_collapsed_cells(cells)

        for _ in range(len(cells)):
            # remove collapsed cells
            cells = self._prune_collapsed_cells(cells)
            if len(cells) == 0:
                break

            # choose cell with least entropy
            min_cells = self.get_min_cells(cells)
            cell = random.choice(min_cells)

            # collapse cell
            row, column = cell.get_coordinates()
            chosen_tile = self.cell_manager.collapse(row, column)

            # update surrounding cells
            if chosen_tile is not None:
                self.cell_manager.reduce_possibilities_for(row, column, chosen_tile)

            # update canvas and sleep
            if update_canvas is True:
                self.cell_manager.canvas.update_idletasks()
                sleep(self.delay)


    def check_invalid(self) -> None:
        '''
        Check if any cell is invalid(tile_set_size == 0) and collapse it
        without updating neighboring cells.
        '''
        cells = self._get_cells()
        cells = [cell for cell in cells if cell.get_tile_set_size() == 0]

        for cell in cells:
            row, column = cell.get_coordinates()
            self.cell_manager.collapse(row, column)


    def _get_cells(self) -> list[Cell]:
        '''
        Return cells from the cell_manager,
        flattened from a matrix to a list.
        '''
        return [
            cell
            for cell_row
            in self.cell_manager.cells
            for cell
            in cell_row
        ]


    def get_min_cells(self, cells: list[Cell]) -> list[Cell]:
        '''
        Returns a list of cells with smallest tile_set size.
        '''
        # sort cells by tile set length ASC
        min_cell_score = self._get_min_cells_score(cells)

        return [
            cell
            for cell
            in cells
            if cell.get_tile_set_size() != 0 and
               cell.get_tile_set_size() == min_cell_score
        ]


    def _get_min_cells_score(self, cells: list[Cell]) -> int:
        '''
        Returns the smallest tile set size in cells.
        '''
        return min(
            cell.get_tile_set_size()
            for cell
            in cells
        )


    def _prune_collapsed_cells(self, cells: list[Cell]) -> list[Cell]:
        '''
        Returns a modified list of cells, where
        cells aren't collapsed and arne't empty.
        '''
        return [
            cell
            for cell
            in cells
            if cell.get_tile_set_size() != -1 and
               cell.get_tile_set_size() != 0
        ]
