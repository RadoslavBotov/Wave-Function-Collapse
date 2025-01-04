import random

from PIL import Image, ImageTk


class Cell:
    DEFAULT_BACKGROUND_COLOR = 'gray'
    
    def __init__(self, x, y, size, canvas, possibilities = []):
        self.x = y
        self.y = x
        self.size = size
        self.canvas = canvas
        self.possibilities = possibilities # TODO: should be of type Tile
        self.image = ImageTk.PhotoImage(Image.new('RGB', (self.size, self.size), color=Cell.DEFAULT_BACKGROUND_COLOR))
        self.image_id = canvas.create_image(self.x * self.size, self.y * self.size, image=self.image, anchor='nw')
        self.text_id = canvas.create_text(self.x * self.size + self.size//2, self.y * self.size + self.size//2, text=str(len(self.possibilities)), anchor='center')
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
        if self.x != highlight_data.last_row or self.y != highlight_data.last_column:
            highlight_data.last_row = self.x
            highlight_data.last_column = self.y

            cur_rect = self.canvas.create_rectangle(self.x * self.size, self.y * self.size, self.x  * self.size + self.size, self.y  * self.size + self.size)

            if highlight_data.last_rect is not None:
                self.canvas.delete(highlight_data.last_rect)

            highlight_data.last_rect = cur_rect