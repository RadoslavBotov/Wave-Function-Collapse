from src.cells.cell_manager_base import CellManagerBase
from tests.mocks.cell_mock import CellMock


class CellManagerMock(CellManagerBase):
    def __init__(self,
                 rows: int,
                 columns: int,
                 cell_size: tuple[int, int]) -> None:
        super().__init__(rows, columns, cell_size)


    def init_cells(self, cells):
        self.cells = cells
