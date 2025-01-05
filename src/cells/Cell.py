import random
from tkinter import Canvas

from PIL import Image, ImageTk

from src.tiles.tile_set import TileSet


class Cell:
    DEFAULT_BACKGROUND_COLOR = 'gray'
    
    def __init__(self, row, column, cell_size: int, canvas: Canvas, possibilities: TileSet):
        self.row = column
        self.column = row
        self.cell_size = cell_size
        self.canvas = canvas
        self.possibilities = possibilities # TODO: should be of type Tile
        self.image = ImageTk.PhotoImage(Image.new('RGB', (self.cell_size, self.cell_size), color=Cell.DEFAULT_BACKGROUND_COLOR))
        self.image_id = canvas.create_image(self.row * self.cell_size, self.column * self.cell_size, image=self.image, anchor='nw')
        self.text_id = canvas.create_text(self.row * self.cell_size + self.cell_size//2, self.column * self.cell_size + self.cell_size//2, text=str(len(self.possibilities)), anchor='center')
        self._is_collapsed = False


    def collapse(self):
        if self._is_collapsed is False:
            tile = self.possibilities[random.randrange(len(self.possibilities))]

            self.possibilities = tile
            self.image = ImageTk.PhotoImage(tile.image)

            self.canvas.itemconfig(self.image_id, image=self.image)
            self.canvas.delete(self.text_id)
        
        self._is_collapsed = True


    def reduce_possibilities(self, other, direction):
        if self._is_collapsed is False:
            self.possibilities = [tile for tile in self.possibilities if tile.does_side_code_match(other.possibilities, direction=direction)]
            self.canvas.itemconfig(self.text_id, text=str(len(self.possibilities)))


    def highlight(self, highlight_data):
        if self.row != highlight_data.last_row or self.column != highlight_data.last_column:
            highlight_data.last_row = self.row
            highlight_data.last_column = self.column

            cur_rect = self.canvas.create_rectangle(self.row * self.cell_size, self.column * self.cell_size, self.row  * self.cell_size + self.cell_size, self.column  * self.cell_size + self.cell_size)

            if highlight_data.last_rect is not None:
                self.canvas.delete(highlight_data.last_rect)

            highlight_data.last_rect = cur_rect
