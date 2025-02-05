from src.cells.cell_base import CellBase


class CellMock(CellBase):
    def __init__(self,
                 row: int,
                 column: int,
                 cell_size: tuple[int, int],
                 tile_set_size: int = -1) -> None:
        super().__init__(row, column, cell_size)
        self.tile_set_size = tile_set_size

 
    def get_tile_set_size(self) -> int:
        return self.tile_set_size
