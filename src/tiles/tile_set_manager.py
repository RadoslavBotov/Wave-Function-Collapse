import os
from pathlib import Path

from src.tiles.tile_set import TileSet
from src.readers.readers import read_config_file, read_images
from src.readers.formatter import ConfigFormatter


class TileSetManager(dict):
    def __init__(self, *arg, **kw):
        super(TileSetManager, self).__init__(*arg, **kw)


    @classmethod
    def create_tile_set_manager(cls, tile_set_directory_path: str|Path) -> 'TileSetManager':
        tile_set_dirs = [ts for ts in os.listdir(tile_set_directory_path) if ts.endswith('tile_set')]

        tile_sets = TileSetManager()

        for tile_set_name in tile_set_dirs:
            tile_set_configs = read_config_file(os.path.join(tile_set_directory_path, tile_set_name, 'tile_descriptions.yaml'))
            tile_set_formatted_configs = ConfigFormatter.format_configs_for_images(tile_set_configs)

            tile_set_images = read_images(os.path.join(tile_set_directory_path, tile_set_name))

            tile_set = TileSet.create_tile_set(tile_set_formatted_configs, tile_set_images)

            tile_sets[tile_set_name] = (tile_set)

        return tile_sets


if __name__ == '__main__':
    TileSetManager.create_tile_set_manager('tilesets')