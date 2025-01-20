import os
import sys
import tkinter as tk

from pathlib import Path
from tkinter import filedialog

from src.formatters.image_config_formatter import format_image_configs
from src.readers.yaml_reader import read_config_file
from src.readers.image_reader import read_images
from src.cells.cell_manager import CellManager
from src.tiles.tile_set_manager import TileSetManager
from src.tiles.tile_set import TileSet


# TODO: refactor to config file
N = 10
K = 10
M = (40, 40)

tile_path = Path('tilesets')
tile_set = Path('default_tile_set')

def highlightCell(event, cell_manager: CellManager):
    row, column = cell_manager.getCellIndices(event.x, event.y)
    cell_manager.highlight_cell(row, column)


def collapse(event, cell_manager: CellManager):
    row, column = cell_manager.getCellIndices(event.x, event.y)
    chosen_tile = cell_manager.collapse(row, column)
    if chosen_tile is not None:
        cell_manager.reduce_possibilities_for(row, column, chosen_tile)


def save_image():
    file_types = [('png', '*png'), ('.jpeg', '*.jpeg')]
    
    file = filedialog.asksaveasfilename(title='Save Current Image As',
                                        filetypes=file_types,
                                        initialdir=os.getcwd())
    
    if file != '':
        # print(file)
        pass


def chose_tile_set(bool_variable, tile_set_name, cell_manager):
    print(tile_set_name)
    cell_manager.switch_tile_sets_with(bool_variable, tile_set_name)


def show_extra_cell_information(bool_variable, cell_manager):
    if bool_variable.get() is True:
        cell_manager.enable_cell_extra_information()
    else:
        cell_manager.disable_cell_extra_information()


def main():
    # correct paths
    cwd = Path.cwd()                         # current working directory
    entry_point = Path(sys.argv[0])          # path to main when starting program
    path_to_main = cwd.joinpath(entry_point) # ../WFC/src/main.py
    path_to_wfc = path_to_main.parent # ../WFC/
    path_to_tiles = path_to_wfc.joinpath(tile_path)  # ../WFC/tilesets

    # Create root
    # wfc = WaveFunctionCollapse()
    # wfc.mainloop()

    res = read_config_file(Path('configs.yaml'))
    print(res)
    
    root = tk.Tk()
    root.geometry(f'{N*40}x{N*40}')
    root.resizable(False, False)

    # Create canvas
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.configure(bg='grey')

    # Load images and their configs

    # Create tile set manager
    tile_set_dirs = [ts for ts in os.listdir(path_to_tiles) if ts.endswith('tile_set')]
    tile_sets = dict()

    for tile_set_name in tile_set_dirs:
        tile_set_configs = read_config_file(Path(tile_path, tile_set_name, f'{tile_set_name}.yaml'))
        
        tile_set_formatted_configs = format_image_configs(tile_set_configs)

        tile_set_images = read_images(Path(tile_path, tile_set_name))

        tile_set = TileSet.create_tile_set(tile_set_formatted_configs, tile_set_images)

        tile_sets[tile_set_name] = tile_set 
    
    tsm = TileSetManager(tile_sets)

    # Create tkinter variables
    show_extra_information = tk.BooleanVar()
    show_extra_information.set(False)
    
    # Create cells
    cm = CellManager(N, K, M, canvas, tsm)
    cm.switch_tile_sets_with(show_extra_information)
    #cells = cm.cells
    
    # TODO: Create menus
    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="save as", command=save_image)
    menubar.add_cascade(menu = file_menu, label = "File")

    tile_set_menu = tk.Menu(menubar, tearoff=0)
    for tile_set_name in tsm:
        tile_set_menu.add_command(label=tile_set_name, command=lambda sei=show_extra_information, tsm=tile_set_name: chose_tile_set(sei, tsm, cm))
    menubar.add_cascade(menu=tile_set_menu, label = "Tile Sets")
    
    cell_menu = tk.Menu(root, tearoff=0)
    cell_menu.add_command(label='Show grid')
    cell_menu.add_checkbutton(label='Show extra information', onvalue=1, offvalue=0, variable=show_extra_information, command=lambda: show_extra_cell_information(show_extra_information, cm))
    menubar.add_cascade(menu=cell_menu, label = "Cells")

    root.config(menu=menubar)

    # Bind event
    canvas.bind('<Button-1>', lambda event: collapse(event, cm))
    root.bind('<Motion>', lambda event: highlightCell(event, cm))
    
    # Start mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
