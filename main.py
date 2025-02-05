import os
import tkinter as tk

from pathlib import Path
from tkinter import filedialog
from PIL import Image

from src.formatters.image_config_formatter import format_image_configs
from src.formatters.wfc_config_formatter import format_wfc_configs
from src.readers.yaml_reader import read_config_file
from src.readers.image_reader import read_images
from src.cells.cell_manager import CellManager
from src.solver.solver import Solver
from src.tiles.tile import Tile
from src.tiles.tile_set_manager import TileSetManager
from src.tiles.tile_set import TileSet


def highlightCell(event, cell_manager: CellManager):
    row, column = cell_manager.get_cell_indices(event.x, event.y)
    cell_manager.highlight_cell(row, column)


def collapse(event, cell_manager: CellManager):
    row, column = cell_manager.get_cell_indices(event.x, event.y)
    chosen_tile = cell_manager.collapse(row, column)
    if chosen_tile is not None:
        cell_manager.reduce_possibilities_for(row, column, chosen_tile)


def save_image(cell_manager: CellManager):
    file_types = [('png', '*.png'), ('jpeg', '*.jpeg')]
    
    file = filedialog.asksaveasfilename(title='Save Current Image As',
                                        filetypes=file_types,
                                        initialdir=os.getcwd(),
                                        defaultextension="*.*")
    
    if file != '':
        image = cell_manager.get_current_image()
        image.save(file)


def chose_tile_set(bool_variable, tile_set_name, cell_manager):
    print(tile_set_name)
    cell_manager.switch_tile_sets_with(bool_variable, tile_set_name)


def show_extra_cell_information(bool_variable, cell_manager):
    if bool_variable.get() is True:
        cell_manager.enable_cell_extra_information()
    else:
        cell_manager.disable_cell_extra_information()


def solver_csp(cell_manager: CellManager, delay):
    solver = Solver(cell_manager, delay)
    solver.start()
    solver.check_invalid()


def create_tile_set(configs: dict, images: dict[str, Image.Image]) -> TileSet:
    tiles = []

    for image_name in configs:
        image_configs = configs[image_name]
        side_codes = image_configs['directions']

        original_tile = Tile(images[image_name], side_codes)
        tiles.append(original_tile)

        for rotations_amount, rotation_direction in image_configs['rotations']:
            rotated_tile = Tile(images[image_name], side_codes)
            rotated_tile.rotate_tile(rotations_amount, rotation_direction)
            tiles.append(rotated_tile)

    return TileSet(tiles)


def create_tile_set_manager(path_to_tiles: Path) -> TileSetManager:
    tile_set_dirs = [ts for ts in os.listdir(path_to_tiles) if ts.endswith('tile_set')]
    tile_sets = {}

    for tile_set_name in tile_set_dirs:
        tile_set_configs = read_config_file(Path(path_to_tiles, tile_set_name, f'{tile_set_name}.yaml'))
        
        tile_set_formatted_configs = format_image_configs(tile_set_configs)

        tile_set_images = read_images(Path(path_to_tiles, tile_set_name))

        tile_set = create_tile_set(tile_set_formatted_configs, tile_set_images)

        tile_sets[tile_set_name] = tile_set 
    
    return TileSetManager(tile_sets)


def create_tkinter_widgets(rows, column, size):
    # Create root window
    root = tk.Tk()
    root.geometry(f'{rows*size[0]}x{column*size[1]}')
    root.resizable(False, False)

    # Create canvas
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.configure(bg='grey')

    return root, canvas


def create_menus(root, cell_manager, tile_set_manager, show_extra_information, delay):
    # Menus
    menubar = tk.Menu(root)

    # Menu for saving image
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="save as", command=lambda cm=cell_manager:save_image(cm))
    menubar.add_cascade(menu = file_menu, label = "File")

    # Menu for switching tile sets
    tile_set_menu = tk.Menu(menubar, tearoff=0)
    for tile_set_name in tile_set_manager:
        tile_set_menu.add_command(label=tile_set_name,
                                  command=lambda sei=show_extra_information,
                                  tile_set_manager=tile_set_name: chose_tile_set(sei, tile_set_manager, cell_manager))
    menubar.add_cascade(menu=tile_set_menu, label = "Tile Sets")
    
    # Menu for showing extra cell information on canvas
    cell_menu = tk.Menu(root, tearoff=0)
    cell_menu.add_checkbutton(label='Show extra information',
                              onvalue=1,
                              offvalue=0,
                              variable=show_extra_information,
                              command=lambda: show_extra_cell_information(show_extra_information, cell_manager))
    menubar.add_cascade(menu=cell_menu, label = "Cells")

    # Menu for starting solver
    solver_menu = tk.Menu(root, tearoff=0)
    solver_menu.add_command(label='Start solver',
                          command=lambda: solver_csp(cell_manager, delay))
    menubar.add_cascade(menu=solver_menu, label = "Solver")

    root.config(menu=menubar)
    
    return show_extra_information


def main():
    # Load and format default configs
    configs = read_config_file(Path('configs.yaml'))
    configs = format_wfc_configs(configs)
    
    # get all default configs
    default_tile_path = configs['default_tile_path']
    default_cell_rows = configs['default_cell_rows']
    default_cell_columns = configs['default_cell_columns']
    default_cell_size = configs['default_cell_size']
    default_solver_delay = configs['default_solver_delay']
    
    # Get path to directory with TileSets
    path_to_tiles = Path(default_tile_path)

    # Create tkinter window and gadgets
    root, canvas = create_tkinter_widgets(default_cell_rows,
                                          default_cell_columns,
                                          default_cell_size)

    # Create managers
    tile_set_manager = create_tile_set_manager(path_to_tiles)
    
    cell_manager = CellManager(default_cell_rows,
                               default_cell_columns,
                               default_cell_size,
                               canvas,
                               tile_set_manager)
    
    # Create tkinter variables
    show_extra_information = tk.BooleanVar()
    show_extra_information.set(False)
    
    # Create menus
    create_menus(root, cell_manager, tile_set_manager, show_extra_information, default_solver_delay)

    # Bind events
    cell_manager.switch_tile_sets_with(show_extra_information)
    canvas.bind('<Button-1>', lambda event: collapse(event, cell_manager))
    root.bind('<Motion>', lambda event: highlightCell(event, cell_manager))
    
    # Start mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
