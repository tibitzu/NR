import numpy as np  # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[0:80, 0] = tile_types.wall
        self.tiles[0:80, 44] = tile_types.wall
        self.tiles[0, 0:45] = tile_types.wall
        self.tiles[79, 0:45] = tile_types.wall

        self.tiles[33, 10] = tile_types.open_door

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
