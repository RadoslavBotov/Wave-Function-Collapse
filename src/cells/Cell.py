import random
from tkinter import Canvas

from PIL import ImageTk

from src.constants import ERROR_BACKGROUND_TILE
from src.direction import Direction
from src.tiles.tile_set import TileSet
from src.tiles.tile import Tile


class Cell:
    def __init__(self, row: int, column: int, cell_size: int|tuple[int, int], tile_set: TileSet, canvas: Canvas) -> None:
        '''
        - row - row in grid
        - column - column in grid
        - cell_size - cell size
        - tile_set - TileSet from which Tiles are chosen
        - canvas - tkinter canvas to draw on
        '''
        self.row = row
        self.column = column
        self.cell_size = cell_size if isinstance(cell_size, tuple) else (cell_size, cell_size)
        self.tile_set = tile_set
        self.canvas = canvas

        '''
        + _chosen_tile - allows image to be resized
        + _chosen_image - PhotoImage reference, so that canvas displays image
        + _image_id - image id in canvas
        + _text_id - text id in canvas
        + _is_collapsed - tile was chosen to display image or not
        '''
        self._chosen_tile: Tile|None = None
        self._chosen_image: ImageTk.PhotoImage|None = None
        self._image_id: int|None = None
        self._text_id: int|None = None
        self._is_collapsed: bool = False


    def update_tile_sizes(self) -> None:
        '''
        Updates size of images in TileSet to @cell_size.
        '''
        if self.cell_size != self.tile_set.get_tile_image_size():
            self.tile_set.resize_tiles(self.cell_size)


    def collapse(self) -> Tile|None:
        '''
        Chose of the the possible Tile's from the TileSet.
        
        If Cell is already collapsed, returns None.
        If Cell has no Tile's to chose from, returns ERROR_BACKGROUND_TILE.
        If there are no possibilities (len(TileSet) == 0), chose the ERROR_BACKGROUND_IMAGE.
        If cell is already collapsed, returns None.
        Otherwise, returns a random Tile's from TileSet.
        '''
        if self._is_collapsed is True:
            return None

        self._is_collapsed = True
        
        if len(self.tile_set) == 0:
            tile = ERROR_BACKGROUND_TILE 
        else:
            tile = random.choice(self.tile_set)

        return tile


    def reduce_possibilities(self, tile_to_match: Tile, self_direction: Direction, other_direction: Direction) -> int|None:
        '''
        Removes Tile's from TileSet, whose sides_code do not match
        the sides_code of tile_to_match on the given direction.
        
        If Cell is collapsed, does not reduce possibilities, as it's not needed.
        
        - tile_to_match - tile whose sides_code are matched to TileSet
        - direction - Direction of side on @tile_to_match, that we match on
        '''
        if self._is_collapsed is True:
            return None

        reduced_set = self.tile_set.get_reduced_tile_set(tile_to_match, self_direction, other_direction)
        self.tile_set = reduced_set
        print('!')


    def update(self):
        if self._text_id is not None:
            # self.canvas.itemconfig(self._text_id, text=len(self.tile_set))
            return self._text_id


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
