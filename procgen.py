import random

from typing import Iterator, Tuple

import tcod

from game_map import GameMap
import tile_types


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self,) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self,) -> Tuple[slice, slice]:
        # Return the inner area of this room as a 2d array index
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


def road_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_gates(map_width, map_height) -> GameMap:
    gate = GameMap(map_width, map_height)
    gate_direction = random.random()

    if gate_direction < 0.5:
        gate_1 = RectangularRoom(x=39, y=-1, width=4, height=2)
        gate_2 = RectangularRoom(x=39, y=43, width=4, height=2)
    else:
        gate_1 = RectangularRoom(x=-1, y=21, width=2, height=4)
        gate_2 = RectangularRoom(x=78, y=21, width=2, height=4)

    """ Hoping to added further functionality
    elif gate_direction < 0.5:
        gate_1 = RectangularRoom(x=39, y=-1, width=4, height=2, y_axis=True)
        gate_2 = RectangularRoom(x=-1, y=23, width=2, height=4, y_axis=False)
    elif gate_direction < 0.67:
        gate_1 = RectangularRoom(x=39, y=-1, width=4, height=2, y_axis=True)
        gate_2 = RectangularRoom(x=78, y=23, width=2, height=4, y_axis=False)
    elif gate_direction < 0.83:
        gate_1 = RectangularRoom(x=39, y=43, width=4, height=2, y_axis=True)
        gate_2 = RectangularRoom(x=78, y=23, width=2, height=4, y_axis=False)
    else:
        gate_1 = RectangularRoom(x=39, y=43, width=4, height=2, y_axis=True)
        gate_2 = RectangularRoom(x=-1, y=23, width=2, height=4, y_axis=False)
    """




    gate.tiles[gate_1.inner] = tile_types.gate
    gate.tiles[gate_2.inner] = tile_types.gate

    for x, y in road_between(gate_2.center, gate_1.center):
        gate.tiles[x, y] = tile_types.dirt_road

    return gate


def generate_house(map_width, map_height,) -> GameMap:
    house = GameMap(map_width, map_height)

    house_1 = RectangularRoom(x=32, y=15, width=10, height=10)

    house.tiles[house_1.inner] = tile_types.wall

    return house
