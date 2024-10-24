import random
from PIL import Image, ImageTk

class Cell:
   def __init__(self, x, y, size, canvas, possibilities = [], background = None):
      self.x = y
      self.y = x
      self.size = size
      self.canvas = canvas
      self.possibilities = possibilities # TODO: should be of type Tile
      self.image = ImageTk.PhotoImage(Image.new('RGB', (self.size, self.size), color='gray')) if background is None else background
      self.tagroid_image = canvas.create_image(self.x * self.size, self.y * self.size, image=self.image, anchor='nw')
      self.tagroid_text = canvas.create_text(self.x * self.size + self.size//2, self.y * self.size + self.size//2, text=str(len(self.possibilities)), anchor='center')
      self._collapsed = False

   def collapse(self):
      if self._collapsed == False:
         tile = self.possibilities[random.randrange(len(self.possibilities))]

         self.possibilities = tile
         self.image = ImageTk.PhotoImage(tile.image)

         self.canvas.itemconfig(self.tagroid_image, image=self.image)
         self.canvas.delete(self.tagroid_text)
      
      self._collapsed = True

   def reduce_possibilities(self, other, direction):
      if self._collapsed == False:
         self.possibilities = [tile for tile in self.possibilities if tile.rules_match(other.possibilities, direction=direction)]
         self.canvas.itemconfig(self.tagroid_text, text=str(len(self.possibilities)))

   def highlight(self, highligh_data):
      if self.x != highligh_data.last_row or self.y != highligh_data.last_column:
         highligh_data.last_row = self.x
         highligh_data.last_column = self.y

         cur_rect = self.canvas.create_rectangle(self.x * self.size, self.y * self.size, self.x  * self.size + self.size, self.y  * self.size + self.size)

         if highligh_data.last_rect is not None:
               self.canvas.delete(highligh_data.last_rect)

         highligh_data.last_rect = cur_rect