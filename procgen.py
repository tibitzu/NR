from __future__ import annotations

import random

from typing import Iterator, List, Tuple, TYPE_CHECKING

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

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )
    
    
def road_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    # random.random() < 0.5:  # 50% chance.
    # Move horizontally, then vertically.
    corner_x, corner_y = x2, y1
    # else:
    # Move vertically, then horizontally.
    #    corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_town(map_width, map_height, max_houses, house_min_size, house_max_size, ) -> GameMap:
    # Generate a new town map
    town = GameMap(map_width, map_height)
    gate_position_x = random.randint(0, 80)
    gate_position_y = random.randint(0, 42)
    gate_direction = random.random()
    if gate_direction < 0.17:
        gate_1 = RectangularRoom(x=gate_position_x, y=-1, width=4, height=2)
        gate_2 = RectangularRoom(x=gate_position_x, y=43, width=4, height=2)
    elif gate_direction < 0.35:
        gate_1 = RectangularRoom(x=-1, y=gate_position_y, width=2, height=4)
        gate_2 = RectangularRoom(x=78, y=gate_position_y, width=2, height=4)
    elif gate_direction < 0.35:
        gate_1 = RectangularRoom(x=gate_position_x, y=-1, width=4, height=2)
        gate_2 = RectangularRoom(x=-1, y=gate_position_y, width=2, height=4)
    elif gate_direction < 0.67:
        gate_1 = RectangularRoom(x=gate_position_x, y=-1, width=4, height=2)
        gate_2 = RectangularRoom(x=78, y=gate_position_y, width=2, height=4)
    elif gate_direction < 0.83:
        gate_1 = RectangularRoom(x=gate_position_x, y=43, width=4, height=2)
        gate_2 = RectangularRoom(x=78, y=gate_position_y, width=2, height=4)
    else:
        gate_1 = RectangularRoom(x=gate_position_x, y=43, width=4, height=2)
        gate_2 = RectangularRoom(x=-1, y=gate_position_y, width=2, height=4)

    town.tiles[gate_1.inner] = tile_types.gate
    town.tiles[gate_2.inner] = tile_types.gate

    for x, y in road_between(gate_2.center, gate_1.center):
        town.tiles[x, y] = tile_types.dirt_road

    houses: List[RectangularRoom] = []

    for r in range(max_houses):
        house_width = random.randint(house_min_size, house_max_size)
        house_height = random.randint(house_min_size, house_max_size)

        x = random.randint(0, town.width - house_width - 1)
        y = random.randint(0, town.height - house_height - 1)
        
        # "RectangularRoom" class makes rectangles easier to work with
        new_house = RectangularRoom(x, y, house_width, house_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_house.intersects(other_house) for other_house in houses):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        town.tiles[new_house.inner] = tile_types.wall

        houses.append(new_house)

    return town

"""
def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    Generate a new dungeon map.
    dungeon = GameMap(map_width, map_height)

rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.x, player.y = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list.
        rooms.append(new_room)
        
"""
