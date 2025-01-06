from src.tiles.tile_set import TileSet


class TileSetManager(dict[str, TileSet]):
    def __init__(self, *arg, **kw):
        super(TileSetManager, self).__init__(*arg, **kw)


    def get_tile_image_size(self) -> None|int:
        if len(self) == 0:
            return None

        return list(self.values())[0].get_tile_image_size()
