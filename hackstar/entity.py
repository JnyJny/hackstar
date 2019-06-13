"""
"""
from loguru import logger
import tcod

from dataclasses import dataclass


@dataclass
class Entity:
    x: int
    y: int
    onscreen: str
    color: int

    def __str__(self):
        return self.onscreen[0]

    def move(self, dx: int, dy: int) -> None:
        """
        :param int dx:
        :param int dy:
        :return: Tuple[int, int]
        """
        x, y = self.x, self.y
        self.x += dx
        self.y += dy
        return (x, y)

    def erase(self, console, blank: str = " ", x: int = None, y: int = None) -> None:
        """Erase this entity at it's current coords.
        :param tcod.Console console:
        :param str blank:
        :param int x:
        :param int y:
        """
        x = x or self.x
        y = y or self.y

        tcod.console_put_char(console, x, y, blank, tcod.BKGND_NONE)

    def draw(self, console: int = 0, blank=True) -> None:
        """Draw this entity at it's (x,y) coordinates on the specified console.
        """
        tcod.console_set_default_foreground(console, self.color)
        tcod.console_put_char(console, self.x, self.y, str(self), tcod.BKGND_NONE)

    def move_and_draw(self, dx: int, dy: int, console: int = 0) -> None:

        self.erase(console)
        self.x += dx
        self.y += dy
        self.draw(console)
