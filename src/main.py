import tkinter as tk

from tiles.TileManager import TileManager
from cells.CellManager import CellManager

N = 8
M = 40
resource_path = 'resources/basic_tiles'
tile_path = 'resources/basic_tiles_with_rotations'
tile_descriptions = 'tile_descriptions.yaml'

def highlightCell(event, cell_manager):
    cell_manager.highlight_cell(event.x, event.y)

def collapse(event, cell_manager):
    cell_manager.collapse(event.x, event.y)

if __name__ == '__main__':
    # Create root
    root = tk.Tk()
    root.geometry(f'{N*M}x{N*M}')
    root.resizable(False, False)

    # Create canvas
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create base tiles
    tm = TileManager(M, tile_path, tile_descriptions)
    tm.create_tiles()
    tiles = tm.tiles
    
    # Create cells
    cm = CellManager(N, M, canvas, tiles)
    #cells = cm.cells

    # Bind event
    canvas.bind('<Button-1>', lambda event: collapse(event, cm))
    root.bind('<Motion>', lambda event: highlightCell(event, cm))
    
    # Start mainloop
    root.mainloop()