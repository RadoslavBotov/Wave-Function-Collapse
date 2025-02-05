from src.cells.cell_base import CellBase


class CellManagerBase():
    def __init__(self,
                 rows: int,
                 columns: int,
                 cell_size: tuple[int, int]) -> None:
        self.cells: list[list[CellBase]] = []
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
