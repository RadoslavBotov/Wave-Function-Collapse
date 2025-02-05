from src.tiles.tile_set import TileSet


class CellBase:
    def __init__(self,
                 row: int,
                 column: int,
                 cell_size: tuple[int, int]) -> None:
        self.row = row
        self.column = column
        self.cell_size = cell_size
