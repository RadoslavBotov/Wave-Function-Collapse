from cells.Cell import Cell
from cells.HighlightData import HighlightData
from cells.Direction import Direction

class CellManager:
    def __init__(self, dim, size, canvas, possibilities = []):
        self.cells = []
        self.dim = dim
        self.size = size
        for row in range(dim):
            temp = []
            for column in range(dim):
                temp.append(Cell(row, column, size, canvas, possibilities=possibilities))
            self.cells.append(temp)

        self._highlight_data = HighlightData()
        self._moves = [(-1, 0, Direction.north), (0, 1, Direction.east), (1, 0, Direction.south), (0, -1, Direction.west)]

    def highlight_cell(self, x, y):
        row, column = self.getCellIndex(x, y)
        if 0 <= row < self.dim and 0 <= column < self.dim:
            self.cells[row][column].highlight(self._highlight_data)

    def collapse(self, x, y):
        row, column = self.getCellIndex(x, y)
        cell = self.cells[row][column]
        cell.collapse()
        
        for i, j, dir in self._moves:
            if 0 <= row + i < self.dim and 0 <= column + j < self.dim:
                self.cells[row + i][column + j].reduce_possibilities(cell, dir)
    
    def getCellIndex(self, x, y):
        column = x // self.size
        row = y // self.size
        return row, column