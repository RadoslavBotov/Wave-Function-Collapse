import random
import tkinter as tk

from PIL import Image, ImageTk

from src.cells.direction import Direction
from src.tiles.tile_set import TileSet
from src.tiles.tile import Tile


class Cell:
    ERROR_BACKGROUND_TILE: Tile = Tile(Image.new(mode='RGB', size=(40, 40), color='magenta'))

    def __init__(self, row: int, column: int, cell_size: int|tuple[int, int], canvas: tk.Canvas, tile_set: TileSet) -> None:
        self.row = row
        self.column = column
        self.cell_size = cell_size if isinstance(cell_size, tuple) else (cell_size, cell_size)
        self.canvas = canvas
        self.tile_set = tile_set

        self._chosen_image = None
        self._image_id: int|None = None
        self._text_id: int|None = None
        self._is_collapsed: bool = False


    def collapse(self) -> Tile|None:
        '''
        Chose of the the possible tiles from @tile_set to draw in cell.
        If there are no possibilities (@tile_set has length of 0), chose the ERROR_BACKGROUND_IMAGE.
        If cell is already collapsed, returns None.
        '''
        if self._is_collapsed is True:
            return None

        if len(self.tile_set) == 0:
            tile = Cell.ERROR_BACKGROUND_TILE 
        else:
            tile = random.choice(self.tile_set)

        tile.resize_image(self.cell_size)
        self._is_collapsed = True

        return tile


    def draw(self, tile: Tile) -> None:
        self._chosen_image = ImageTk.PhotoImage(tile.image)

        self._image_id = self.canvas.create_image(
            self.column * self.cell_size[1],
            self.row * self.cell_size[0],
            image=self._chosen_image,
            anchor='nw'
        )

        if self._text_id is not None:
            self.canvas.delete(self._text_id)


    def reduce_possibilities(self, other: Tile, direction: Direction) -> None:
        if self._is_collapsed is True:
            return None

        self.tile_set = [
            tile
            for tile
            in self.tile_set
            if tile.does_sides_code_match(other, direction=direction)
        ]

        if self._text_id is not None:
            self.canvas.itemconfig(self._text_id, text=len(self.tile_set))


    def clear(self):
        if self._image_id is not None:
            self.canvas.delete(self._image_id)
        
        if self._text_id is not None:
            self.canvas.delete(self._text_id)


    def highlight(self, highlight_data):
        if highlight_data.check_match(self.row, self.column):
            return None

        cell_size_width = self.cell_size[0]
        cell_size_height = self.cell_size[1]

        cur_rect = self.canvas.create_rectangle(
            self.column * cell_size_height,
            self.row * cell_size_width,
            self.column  * cell_size_height + cell_size_height,
            self.row  * cell_size_width + cell_size_width
        )

        if highlight_data.last_rect is not None:
            self.canvas.delete(highlight_data.last_rect)

        highlight_data.update(self.row, self.column,cur_rect)


    def enable_extra_information(self):
        if self._is_collapsed is True:
            return None
        
        if self._text_id is not None:
            return None
        
        self._text_id = self.canvas.create_text(
            self.column * self.cell_size[1] + self.cell_size[1] // 2,
            self.row * self.cell_size[0] + self.cell_size[0] // 2,
            text=len(self.tile_set),
            anchor='center'
        )


    def disable_extra_information(self):
        if self._text_id is not None:
            self.canvas.delete(self._text_id)
            self._text_id = None
