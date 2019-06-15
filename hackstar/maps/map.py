"""
"""

import tcod
import random
from loguru import logger

from .tile import Tile
from .rect import Rect


class Map:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.needs_fov_recompute = True

    @property
    def tiles(self):
        try:
            return self._tiles
        except AttributeError:
            pass
        self._tiles = [[Tile(x, y, True) for y in range(self.h)] for x in range(self.w)]
        return self._tiles

    @property
    def rooms(self) -> list:
        try:
            return self._rooms
        except AttributeError:
            pass
        self._rooms = []
        return self._rooms

    def dig_dungeon(self, player, max_rooms=11, min_size=6, max_size=10):
        """
        """
        min_x, max_x = 0, self.w - 1
        min_y, max_y = 0, self.h - 1

        for _ in range(max_rooms):

            room = Rect.random(min_size, max_size, min_x, max_x, min_y, max_y)

            for other_room in self.rooms:
                if room in other_room:
                    break
            else:
                logger.debug(f"Room: {room}")
                self.dig_room(room)
                if len(self.rooms) == 0:
                    player.x, player.y = room.center
                else:
                    room_x, room_y = room.center
                    other_x, other_y = self.rooms[-1].center
                    if random.randint(0, 1) == 1:
                        self.dig_h_hall(other_x, room_x, other_y)
                        self.dig_v_hall(other_y, room_y, room_x)
                    else:
                        self.dig_v_hall(other_y, room_y, other_x)
                        self.dig_h_hall(other_x, room_x, room_y)
                self.rooms.append(room)

    def dig_room(self, room) -> None:
        """
        """
        for x in room.xrange():
            for y in room.yrange():
                try:
                    tile = self.tiles[x][y]
                    tile.blocked = False
                    tile.opaque = False
                except IndexError as err:
                    logger.debug(f"{err} x={x} y={y}")

    def dig_h_hall(self, x0, x1, y):
        """
        """
        for x in range(min(x0, x1), max(x0, x1) + 1):
            t = self.tiles[x][y]
            t.blocked = False
            t.opaque = False

    def dig_v_hall(self, y0, y1, x):
        """
        """
        for y in range(min(y0, y1), max(y0, y1) + 1):
            t = self.tiles[x][y]
            t.blocked = False
            t.opaque = False

    def random_rooms(self, count=4):
        """
        """

        for _ in range(count):
            x = random.randint(1, self.w - 2)
            y = random.randint(1, self.h - 2)
            w = random.randint(4, 10)
            h = random.randint(4, 10)
            room = Rect(x, y, w, h)
            self.dig_room(room)

    def is_blocked(self, x: int, y: int) -> bool:
        """
        """
        return self.tiles[x][y].blocked

    def is_opaque(self, x: int, y: int) -> bool:
        """
        """
        return self.tiles[x][y].opaque

    def __iter__(self):
        self._x = 0
        self._y = 0
        return self

    def __next__(self):
        tile = self.tiles[self._x][self._y]
        self._x += 1

        if self._x >= self.w:
            self._x = 0
            self._y += 1

        if self._y >= self.h:
            raise StopIteration()

        return tile

    @property
    def fov_map(self):
        """tcod.Map
        """
        try:
            return self._fov_map
        except AttributeError:
            pass

        self._fov_map = tcod.map_new(self.w, self.h)

        for tile in self:
            tcod.map_set_properties(
                self._fov_map, tile.x, tile.y, not tile.opaque, not tile.blocked
            )
        return self._fov_map

    def recompute_fov(self, x, y, radius, light_walls=True, algorithm=0) -> None:
        """
        """

        if self.needs_fov_recompute:
            logger.debug(
                f"Recomputing FOV for {(x,y)} radius {radius} algorithm:{algorithm}"
            )
            tcod.map_compute_fov(self.fov_map, x, y, radius, light_walls, algorithm)

    def draw(self, console, colors, do_fov=False):
        """
        """

        if not self.needs_fov_recompute and not do_fov:
            return

        for tile in self:

            color = 0x000000
            if tile.is_wall:
                color = colors["dark_wall"]
            if tile.is_floor:
                color = colors["dark_grnd"]
            tcod.console_set_char_background(
                console, tile.x, tile.y, color, tcod.BKGND_SET
            )
