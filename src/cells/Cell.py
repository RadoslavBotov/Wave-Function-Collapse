'''
Cell class
'''
import random
from tkinter import Canvas

from PIL import ImageTk, Image

from src.tiles.tile_set import TileSet
from src.tiles.tile import Tile
from src.constants import ERROR_BACKGROUND_TILE
from src.direction import Direction
from src.highlight_data import HighlightData


class Cell:
    # pylint: disable=too-many-instance-attributes
    '''
    Contains information about its place on a grid,
    a TileSet to choose Tile's from,
    and methods to draw on tk.Canvas.
    '''
    def __init__(self,
                 row: int,
                 column: int,
                 cell_size: int|tuple[int, int],
                 tile_set: TileSet) -> None:
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
        '''
        + _chosen_tile - allows image to be resized (PhotoImage can't be resized nicely)
        + _chosen_image - PhotoImage reference, so that canvas displays image
        + _image_id - PhotoImage id in canvas
        + _text_id - text id in canvas
        + _is_collapsed - tile was chosen to display image or not
        '''
        self._chosen_tile: Tile|None = None
        self._chosen_image: ImageTk.PhotoImage|None = None
        self._image_id: int|None = None
        self._text_id: int|None = None
        self._is_collapsed: bool = False


    def get_tile_set_size(self) -> int:
        '''
        Get size of TileSet.
        
        If Cell is collapsed, return 0.
        '''
        if self._is_collapsed is True:
            return 0

        return len(self.tile_set)


    def get_chosen_image(self, background_color: str = 'white') -> Image.Image:
        '''
        Returns the image chosen when cell was collapsed.
        '''
        if (   self._is_collapsed is False
            or self._chosen_tile is None
            or self._chosen_tile.image is None):
            return Image.new('RGB', self.cell_size, color=background_color)

        return self._chosen_tile.image


    def resize_cell(self, new_cell_size: tuple[int, int]) -> bool:
        '''
        Resizes Cell and TileSet to new_cell_size.
        '''
        self.cell_size = new_cell_size

        if self._chosen_tile is not None:
            self._chosen_tile.resize_image(self.cell_size)

        return self.tile_set.resize_tiles(self.cell_size)


    def collapse(self) -> Tile|None:
        '''
        Chose one of the the possible Tile's from the TileSet.

        If Cell is already collapsed, returns None.
        If Cell has no Tile's to chose from, returns ERROR_BACKGROUND_TILE.
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


    def reduce_tile_set(self, other: Tile,
                        self_direction: Direction,
                        other_direction: Direction) -> int|None:
        '''
        Removes Tile's from TileSet, whose sides_code do not match
        the sides_code of tile_to_match on the given direction.

        If Cell is not collapsed, returns new size of TileSet after reduction.
        If Cell is collapsed, does not reduce possibilities, as it's not needed.

        - other - tile whose sides_code are matched to TileSet
        - self_direction - Direction of side on @self that is matched
        - other_direction - Direction of side on @other that is matched
        '''
        if self._is_collapsed is True:
            return None

        reduced_set = self.tile_set.get_reduced_tile_set(other, self_direction, other_direction)
        self.tile_set = reduced_set

        return len(self.tile_set)


    def draw(self, tile: Tile, canvas: Canvas) -> None:
        '''
        Draws given Tile on Canvas, with respect to the Cell's grid
        coordinates and cell_size.
        '''
        self._chosen_tile = tile
        self._chosen_image = ImageTk.PhotoImage(tile.image)

        self._image_id = canvas.create_image(
            self.column * self.cell_size[1],
            self.row * self.cell_size[0],
            image=self._chosen_image,
            anchor='nw'
        )

        # remove extra information from cell on draw
        if self._text_id is not None:
            canvas.delete(self._text_id)


    def clear(self, canvas: Canvas) -> None:
        '''
        Clears Cell's image and extra information from canvas
        if they were drawn.
        '''
        if self._image_id is not None:
            canvas.delete(self._image_id)

        if self._text_id is not None:
            canvas.delete(self._text_id)


    def highlight(self, highlight_data: HighlightData, canvas: Canvas) -> None:
        '''
        Draw a rectangle on the Canvas around the Cell that was hovered over,
        with respect to the Cell's grid coordinates and cell_size.
        
        - highlight_data - contains coordinates were to draw the rectangle
        '''
        # draw rectangle only when a new cell is hovered over
        if highlight_data.check_match(self.row, self.column):
            return None

        cell_size_width = self.cell_size[0]
        cell_size_height = self.cell_size[1]

        current_rectangle = canvas.create_rectangle(
            self.column * cell_size_height,
            self.row * cell_size_width,
            self.column  * cell_size_height + cell_size_height,
            self.row  * cell_size_width + cell_size_width
        )

        if highlight_data.last_rect is not None:
            canvas.delete(highlight_data.last_rect)

        highlight_data.update(self.row, self.column, current_rectangle)

        return None


    def update_extra_information(self, canvas: Canvas, tile_set_length: int|None = None) -> None:
        '''
        Updates text for TileSet amount of Cell, if extra information is enabled.
        '''
        if self._text_id is not None and tile_set_length is not None:
            canvas.itemconfig(self._text_id, text=tile_set_length)


    def enable_extra_information(self, canvas: Canvas) -> None:
        '''
        Draws the number of tiles in TileSet on Canvas.
        '''
        if self._is_collapsed is True:
            return None

        if self._text_id is not None:
            return None

        self._text_id = canvas.create_text(
            self.column * self.cell_size[1] + self.cell_size[1] // 2,
            self.row * self.cell_size[0] + self.cell_size[0] // 2,
            text=len(self.tile_set),
            anchor='center'
        )

        return None


    def disable_extra_information(self, canvas: Canvas) -> None:
        '''
        Erases the number of tiles in TileSet drawn on Canvas.
        '''
        if self._text_id is not None:
            canvas.delete(self._text_id)
            self._text_id = None
