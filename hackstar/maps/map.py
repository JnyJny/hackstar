"""
"""

import tcod
import random
from loguru import logger

from .tile import Tile


class Map:
    def __init__(self, width, height):
        self.w = width
        self.h = height

    @property
    def tiles(self):
        try:
            return self._tiles
        except AttributeError:
            pass
        self._tiles = [[Tile(False) for y in range(self.h)] for x in range(self.w)]
        return self._tiles

    def random_walls(self, count=10):
        """
        """
        for _ in range(count):
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            t = self.tiles[x][y]
            t.blocked = True
            t.block_sight = True
            logger.debug(f"{x},{y} blocked {t.blocked} {t.is_wall}")

    def is_blocked(self, x: int, y: int) -> bool:
        """
        """
        return self.tiles[x][y].blocked

    def is_opaque(self, x: int, y: int) -> bool:
        """
        """
        return self.tiles[x][y].block_sight

    def draw(self, console, colors):
        """
        """
        for y in range(self.h):
            for x in range(self.w):
                tile = self.tiles[x][y]
                color = 0x000000
                if tile.is_wall:
                    color = colors["dark_wall"]
                if tile.is_floor:
                    color = colors["dark_grnd"]
                tcod.console_set_char_background(console, x, y, color, tcod.BKGND_SET)
