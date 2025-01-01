import os
import tkinter as tk

from pathlib import Path

from src.readers.config_file_reader import ConfigFileReader
from src.readers.image_file_reader import ImageFileReader
from src.tiles.tile_manager import TileManager
from src.cells.cell_manager import CellManager


# TODO: refactor to config file
N = 8
M = 40

tile_path = Path('tilesets')
tile_set = Path('basic_tiles_with_rotations')
tile_descriptions = Path('tile_descriptions.yaml')


def highlightCell(event, cell_manager):
    cell_manager.highlight_cell(event.x, event.y)


def collapse(event, cell_manager):
    cell_manager.collapse(event.x, event.y)


if __name__ == '__main__':
    # correct paths
    # cwd = Path.cwd()                         # current working directory
    # entry_point = Path(sys.argv[0])          # path to main when starting program
    # path_to_main = cwd.joinpath(entry_point) # ../WFC/src/main.py
    # path_to_wfc = path_to_main.parent # ../WFC/
    # path_to_tiles = tile_path  # ../WFC/tilesets

    # Create root
    root = tk.Tk()
    root.geometry(f'{N*M}x{N*M}')
    root.resizable(False, False)

    # Create canvas
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Load images and their configs
    config_reader = ConfigFileReader()
    configs_loaded = config_reader.read(os.path.join(tile_path, tile_set, tile_descriptions))

    image_reader = ImageFileReader()
    images_loaded = image_reader.read(os.path.join(tile_path, tile_set))

    # Create base tiles
    tm = TileManager(M)
    tm.create_tiles(configs_loaded, images_loaded)
    tiles = tm.tiles
    
    # Create cells
    cm = CellManager(N, M, canvas, tiles)
    #cells = cm.cells

    # Bind event
    canvas.bind('<Button-1>', lambda event: collapse(event, cm))
    root.bind('<Motion>', lambda event: highlightCell(event, cm))
    
    # Start mainloop
    root.mainloop()
